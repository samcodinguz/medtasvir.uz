import cv2
import numpy as np
import tensorflow as tf
from django.core.files.base import ContentFile
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "apps", "analysis", "model", "lung_cnn_4class.h5")

model = tf.keras.models.load_model(MODEL_PATH)

# 4 ta klass nomi — aynan TRAININGdagi tartib:
# {'COVID': 0, 'Fibrosis': 1, 'Normal': 2, 'Pneumonia': 3}
CLASSES = ["COVID-19", "Fibroz", "Sog‘lom", "Pnevmoniya"]


def predict_lung(image):
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0]  # 4 ta probability chiqadi

    # Har bir klass uchun foizga o'tkazish
    probabilities = {CLASSES[i]: float(prediction[i]) for i in range(len(CLASSES))}

    # Eng ehtimolli klass
    diagnosis = CLASSES[np.argmax(prediction)]
    confidence = float(np.max(prediction))

    return diagnosis, confidence, probabilities



def apply_clahe(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    return enhanced

def apply_gaussian(image):
    return cv2.GaussianBlur(image, (5,5), 0)

def apply_median(image):
    return cv2.medianBlur(image, 5)

def apply_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    return th


def save_processed_image(image, filename):
    success, encoded_image = cv2.imencode(".png", image)
    return ContentFile(encoded_image.tobytes(), name=filename)

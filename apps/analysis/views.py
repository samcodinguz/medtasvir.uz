from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.home import utils as home_utils
from .utils import apply_clahe, apply_gaussian, apply_median, apply_threshold, predict_lung, save_processed_image
from .models import ImageProcessingResult
import time
import cv2

def diagnostic(request):

    if request.method == "POST":
        file = request.FILES["image"]

        # 1. Faylni vaqtincha saqlash
        path = default_storage.save("uploads/" + file.name, ContentFile(file.read()))
        full_path = default_storage.path(path)

        # 2. Rasmini o‘qish
        image = cv2.imread(full_path)

        # 3. Preprocessing natijalari
        gaussian = apply_gaussian(image)
        clahe = apply_clahe(image)
        median = apply_median(image)
        threshold = apply_threshold(image)

        # 4. CNN tashxisi
        diagnosis, confidence = predict_lung(image)

        # 5. Preprocessed rasmlarni File formati bilan saqlash
        gaussian_file = save_processed_image(gaussian, "gaussian_" + file.name)
        clahe_file = save_processed_image(clahe, "clahe_" + file.name)
        median_file = save_processed_image(median, "median_" + file.name)
        threshold_file = save_processed_image(threshold, "threshold_" + file.name)

        # 6. Bazaga yozish
        ImageProcessingResult.objects.create(
            original_image=path,
            gaussian_image=gaussian_file,
            clahe_image=clahe_file,
            median_image=median_file,
            threshold_image=threshold_file,
            diagnosis=diagnosis,
            confidence=confidence
        )
        time.sleep(1)
        return redirect('diagnostic')
    
    result = ImageProcessingResult.objects.last()
    
    context = {
        'page_title': 'Diagnostika',
        'result': result

    }
    context.update(home_utils.get_base_context(request))

    return render(request, 'diagnostic.html', context)

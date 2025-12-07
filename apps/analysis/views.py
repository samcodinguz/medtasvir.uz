from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.home import utils as home_utils
from .utils import apply_clahe, apply_gaussian, apply_median, apply_threshold, predict_lung, save_processed_image, is_grayscale
from .models import ImageProcessingResult
import time
import cv2

def diagnostic(request):

    if not request.user.is_authenticated:
        home_utils.messages.error(request, "Hurmatli foydalanuvchi, diagnostika o‘tkazish uchun tizimga kirishingiz yoki ro‘yxatdan o‘tishingiz kerak")
        return redirect('sign-in')

    if request.method == "POST":
        file = request.FILES["image"]
        filename, img_content = home_utils.square_avatar(file)

        

        # 1. Faylni vaqtincha saqlash
        path = default_storage.save("uploads/" + filename, img_content)
        full_path = default_storage.path(path)

        # 2. Rasmini o‘qish
        image = cv2.imread(full_path)

        if not is_grayscale(image):
            home_utils.messages.error(request, "Ushbu rasm tibbiy rentgen tasviri emas, tibbiy rentgen tasvirini yuklang")
            return redirect('diagnostic')

        # 3. Preprocessing natijalari
        gaussian = apply_gaussian(image)
        clahe = apply_clahe(image)
        median = apply_median(image)
        threshold = apply_threshold(image)

        # 4. CNN tashxisi
        diagnosis, confidence, probs = predict_lung(image)

        # 5. Preprocessed rasmlarni File formati bilan saqlash
        gaussian_file = save_processed_image(gaussian, "gaussian_" + file.name)
        clahe_file = save_processed_image(clahe, "clahe_" + file.name)
        median_file = save_processed_image(median, "median_" + file.name)
        threshold_file = save_processed_image(threshold, "threshold_" + file.name)

        # 6. Bazaga yozish
        ImageProcessingResult.objects.create(
            user=request.user,
            original_image=path,
            gaussian_image=gaussian_file,
            clahe_image=clahe_file,
            median_image=median_file,
            threshold_image=threshold_file,
            diagnosis=diagnosis,
            confidence=confidence,
            covid_prob=probs["COVID-19"],
            fibrosis_prob=probs["Fibroz"],
            normal_prob=probs["Sog‘lom"],
            pneumonia_prob=probs["Pnevmoniya"],
        )
        return redirect('diagnostic')
    
    result = ImageProcessingResult.objects.filter(user=request.user).order_by('-created_at').first()
    
    context = {
        'page_title': 'Diagnostika',
        'result': result

    }
    if result:
        context.update({
            'covid_prob': result.covid_prob * 100,
            'fibrosis_prob': result.fibrosis_prob * 100,
            'normal_prob': result.normal_prob * 100,
            'pneumonia_prob': result.pneumonia_prob * 100,
        })
    context.update(home_utils.get_base_context(request))
    
    return render(request, 'diagnostic.html', context)

def diagnostics(request):
    results = ImageProcessingResult.objects.order_by('-created_at')
    
    paginator = home_utils.Paginator(results, 12)
    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)
    pagination_range = home_utils.get_pagination_range(results.number, paginator.num_pages)

    context = {
        'page_title': 'Barcha diagnostikalar ro\'yxati',
        'pagination_range': pagination_range,
        'results': results
    }
    return render(request, 'diagnostics.html', context)

def diagnostic_result(request, item_id):
    result = ImageProcessingResult.objects.filter(id=item_id).first()
    context = {
        'page_title': f'#{ result.id } - { result.diagnosis }',
        'covid_prob': result.covid_prob * 100,
        'fibrosis_prob': result.fibrosis_prob * 100,
        'normal_prob': result.normal_prob * 100,
        'pneumonia_prob': result.pneumonia_prob * 100,
        'result': result
    }
    return render(request, 'result.html', context)

def diagnostic_save(request):

    if not request.user.is_authenticated:
        home_utils.messages.error(request, "Hurmatli foydalanuvchi, diagnostika o‘tkazish uchun tizimga kirishingiz yoki ro‘yxatdan o‘tishingiz kerak")
        return redirect('sign-in')
    
    if request.method == "POST":
        ImageProcessingResult.objects.filter(user=request.user, check_list=False).update(check_list=True)
        home_utils.messages.success(request, "Diagnostik natijalarga saqlandi")
        return redirect('diagnostic')
    
    return redirect('diagnostic')
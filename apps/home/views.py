from django.shortcuts import render
from apps.analysis.models import ImageProcessingResult
from . import utils
def home(request):
    first_four_results = ImageProcessingResult.objects.order_by('created_at')[:4]

    processed_results = []
    for item in first_four_results:
        item.covid_prob = int(round(item.covid_prob * 100)) if item.covid_prob else 0
        item.fibrosis_prob = int(round(item.fibrosis_prob * 100)) if item.fibrosis_prob else 0
        item.normal_prob = int(round(item.normal_prob * 100)) if item.normal_prob else 0
        item.pneumonia_prob = int(round(item.pneumonia_prob * 100)) if item.pneumonia_prob else 0
        
        processed_results.append(item)

    stats = {
        "covid_count": ImageProcessingResult.objects.filter(diagnosis="COVID-19").count(),
        "fibrosis_count": ImageProcessingResult.objects.filter(diagnosis="Fibroz").count(),
        "normal_count": ImageProcessingResult.objects.filter(diagnosis="Sog‘lom").count(),
        "pneumonia_count": ImageProcessingResult.objects.filter(diagnosis="Pnevmoniya").count()
    }

    context = {
        'page_title': 'Tibbiy tasvirlar asosida avtomatik tashxislash platformasi',
         'processed_results': processed_results,
         'stats': stats,
    }

    context.update(utils.get_base_context(request))

    return render(request, 'home.html', context)

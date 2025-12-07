from django.shortcuts import render
from apps.analysis.models import ImageProcessingResult
from . import utils
def home(request):
    first_four_results = ImageProcessingResult.objects.order_by('created_at')[:4]
    context = {
        'page_title': 'Tibbiy tasvirlar asosida avtomatik tashxislash platformasi',
         'first_four_results': first_four_results,
    }

    context.update(utils.get_base_context(request))

    return render(request, 'home.html', context)

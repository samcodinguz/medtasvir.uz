from django.shortcuts import render
from . import utils
def home(request):

    context = {
        'page_title': 'Tibbiy tasvirlar asosida avtomatik tashxislash platformasi',
    }

    context.update(utils.get_base_context(request))

    return render(request, 'home.html', context)

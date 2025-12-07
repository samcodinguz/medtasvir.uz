from django.urls import path
from . import views

urlpatterns = [
    path('diagnostic', views.diagnostic, name='diagnostic'),
]
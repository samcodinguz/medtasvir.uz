from django.urls import path
from . import views

urlpatterns = [
    path('diagnostic', views.diagnostic, name='diagnostic'),
    path('diagnostics', views.diagnostics, name='diagnostics'),
    path('diagnostic/result/<int:item_id>', views.diagnostic_result, name='diagnostic-result'),
    path('diagnostic/save', views.diagnostic_save, name='diagnostic-save'),
]
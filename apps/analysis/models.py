from django.db import models
from apps.users.models import CustomUser
class ImageProcessingResult(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    original_image = models.ImageField(upload_to='uploads/originals/')
    gaussian_image = models.ImageField(upload_to='uploads/gaussian/', null=True, blank=True)
    clahe_image = models.ImageField(upload_to='uploads/clahe/', null=True, blank=True)
    median_image = models.ImageField(upload_to='uploads/median/', null=True, blank=True)
    threshold_image = models.ImageField(upload_to='uploads/threshold/', null=True, blank=True)

    diagnosis = models.CharField(max_length=255, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    # 4 ta klass foizlari
    covid_prob = models.FloatField(null=True, blank=True)
    fibrosis_prob = models.FloatField(null=True, blank=True)
    normal_prob = models.FloatField(null=True, blank=True)
    pneumonia_prob = models.FloatField(null=True, blank=True)

    check_list = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tahlil #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

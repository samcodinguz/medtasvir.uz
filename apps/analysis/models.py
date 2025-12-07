from django.db import models

class ImageProcessingResult(models.Model):
    original_image = models.ImageField(upload_to='uploads/originals/')
    gaussian_image = models.ImageField(upload_to='uploads/gaussian/', null=True, blank=True)
    clahe_image = models.ImageField(upload_to='uploads/clahe/', null=True, blank=True)
    median_image = models.ImageField(upload_to='uploads/median/', null=True, blank=True)
    threshold_image = models.ImageField(upload_to='uploads/threshold/', null=True, blank=True)

    diagnosis = models.CharField(max_length=255, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tahlil #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

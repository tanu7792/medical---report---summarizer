from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    return f"reports/user_{instance.user.id}/{filename}"

class MedicalReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=255, blank=True)
    original_file = models.FileField(upload_to=upload_to, null=True, blank=True)
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title or (self.original_file.name if self.original_file else f"report-{self.id}")

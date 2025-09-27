from django.db import models
from django.conf import settings

def upload_to_report(instance, filename):
    return f"reports/user_{instance.owner.id}/{filename}"

class Report(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=255, blank=True)
    original_file = models.FileField(upload_to=upload_to_report)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="uploaded")

    def __str__(self):
        return f"{self.title or self.original_file.name} ({self.owner.username})"

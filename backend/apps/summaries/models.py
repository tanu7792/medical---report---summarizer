from django.db import models
from apps.reports.models import Report
from django.conf import settings

class Summary(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="summaries")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=100)
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    model_info = models.JSONField(default=dict, blank=True)

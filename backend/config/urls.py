from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse
from apps.reports.views import ReportViewSet
from apps.summaries.views import SummaryViewSet
from apps.users import urls as users_urls

router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="reports")
router.register(r"summaries", SummaryViewSet, basename="summaries")

def home(request):
    return HttpResponse("Welcome to the Medical Report Summarizer API!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include(users_urls)),
    path("api/", include(router.urls)),
    path("", home),  # <-- root URL added
]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse
from apps.reports.views import ReportViewSet
from apps.summaries.views import SummaryViewSet
from apps.users import urls as users_urls

# ✅ Router setup
router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="reports")
router.register(r"summaries", SummaryViewSet, basename="summaries")

# ✅ Define home view right here
def home(request):
    return HttpResponse("✅ Welcome to the Medical Report Summarizer API!")

# ✅ URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include(users_urls)),
    path("api/", include(router.urls)),
    path("", home, name="home"),  # only one home route
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

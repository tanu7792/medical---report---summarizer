from django.urls import path
from .views import SummaryListView

urlpatterns = [
    path("", SummaryListView.as_view(), name="summaries-list"),
]

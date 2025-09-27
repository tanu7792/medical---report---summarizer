from django.urls import path
from .views import RecordDeviceView
urlpatterns = [
    path("record/", RecordDeviceView.as_view(), name="record-device"),
]

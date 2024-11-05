from django.urls import path
from .views import (
    ProcessUserTextAPIView,
)

urlpatterns = [
    path(
        "process-user-text/", ProcessUserTextAPIView.as_view(), name="process-user-text"
    ),
]

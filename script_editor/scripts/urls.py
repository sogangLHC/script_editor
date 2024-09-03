from django.urls import path
from .views import ScriptEditAPIView

urlpatterns = [
    path("edit-script/", ScriptEditAPIView.as_view(), name="edit-script"),
]

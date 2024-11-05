# scripts/urls.py

from django.urls import path
from .views import ScriptEditAPIView, UserScriptLogAPIView, GenerateAnswerAPIView

urlpatterns = [
    path("edit-script/", ScriptEditAPIView.as_view(), name="edit-script"),
    path("user-script-log/", UserScriptLogAPIView.as_view(), name="user-script-log"),
    path(
        "generate-answer/", GenerateAnswerAPIView.as_view(), name="generate-answer"
    ),  # 새로운 엔드포인트 추가
]

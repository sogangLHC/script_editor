from django.urls import path
from .views import ScriptEditAPIView, UserScriptLogAPIView

urlpatterns = [
    path("edit-script/", ScriptEditAPIView.as_view(), name="edit-script"),
    path(
        "my-scripts/", UserScriptLogAPIView.as_view(), name="user-scripts"
    ),  # 사용자별 스크립트 로그 조회 엔드포인트
]

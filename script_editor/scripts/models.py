# scripts/models.py

from django.db import models
from django.contrib.auth.models import User


class Script(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # 사용자와의 foreign 키 관계 설정
    original_text = models.TextField()  # 사용자가 제출한 원본 대본
    edited_text = models.TextField(blank=True, null=True)  # GPT가 수정한 대본
    audience_level = models.CharField(max_length=50, default="general")  # 청중 수준
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    def __str__(self):
        return f"Script by {self.user.username} at {self.created_at}"

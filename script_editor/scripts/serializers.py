from rest_framework import serializers
from .models import Script


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ["id", "original_text", "edited_text", "created_at", "updated_at"]

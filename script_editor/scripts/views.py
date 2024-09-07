# scripts/views.py

import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Script
from .serializers import ScriptSerializer
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기


# 1. gpt에 post 기능
class ScriptEditAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 사용자 인증이 필요한 API로 설정

    def post(self, request):
        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            original_text = serializer.validated_data["original_text"]
            audience_level = serializer.validated_data.get(
                "audience_level", "general"
            )  # 기본값은 'general'로 설정

            # OpenAI API를 호출하여 대본 수정
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # 사용할 GPT 모델
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an assistant that corrects grammatical and meaning errors in scripts for an audience at the '{audience_level}' level.",
                        },
                        {
                            "role": "user",
                            "content": f"Correct the following script for any grammatical or meaning errors:\n\n{original_text}",
                        },
                    ],
                    max_tokens=1000,
                )

                # GPT로부터 수정된 대본 추출
                edited_text = response.choices[0].message["content"].strip()

                # 수정된 대본을 사용자가 인증된 상태에서 저장
                script_instance = Script.objects.create(
                    user=request.user,
                    original_text=original_text,
                    edited_text=edited_text,
                    audience_level=audience_level,  # 청중 수준도 저장
                )

                return Response(
                    ScriptSerializer(script_instance).data,
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. 사용자별 질문 로그 조회
class UserScriptLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 로그인된 사용자의 모든 스크립트 조회
        scripts = Script.objects.filter(user=request.user)
        serializer = ScriptSerializer(scripts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

import openai
from pinecone import Pinecone, Index
from dotenv import load_dotenv
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Script, GrammarRule, ExampleSentence
from .serializers import ScriptSerializer

# 환경 변수 로드
load_dotenv()

# OpenAI 및 Pinecone API 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = os.getenv("PINECONE_HOST")

# Pinecone 초기화   
pc = Pinecone(api_key=pinecone_api_key)
index_name = "grammar-index"
index = Index(name=index_name, api_key=pinecone_api_key, host=pinecone_host)


def create_embedding(text):
    """
    OpenAI API를 사용하여 텍스트 임베딩 생성
    """
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


def retrieve_similar_documents(query, top_k=5, similarity_threshold=0.9):
    """
    사용자의 쿼리와 유사한 문서 검색
    """
    query_embedding = create_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    print("Pinecone Query Results:", results)  # 결과 확인용 출력

    filtered_matches = [
        match for match in results["matches"] if match["score"] >= similarity_threshold
    ]

    matched_texts = [match["metadata"]["text"] for match in filtered_matches]
    explanations = [
        match["metadata"].get("explanation", "") for match in filtered_matches
    ]

    unique_explanations = list(set(filter(None, explanations)))

    return matched_texts, unique_explanations


def retrieve_and_correct_with_gpt_verification(
    query, top_k=5, similarity_threshold=0.8
):
    """
    벡터 DB에서 유사한 문서를 검색한 후, GPT로 추가 검증을 수행하여 최종 수정된 문장과 문법 오류를 생성합니다.
    """
    # Step 1: 벡터 DB 검색
    query_embedding = create_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    # 검색 결과 필터링
    filtered_matches = [
        match for match in results["matches"] if match["score"] >= similarity_threshold
    ]

    matched_texts = [match["metadata"]["text"] for match in filtered_matches]
    explanations = [
        match["metadata"].get("explanation", "") for match in filtered_matches
    ]

    # 중복되지 않은 모든 설명 수집 및 빈 문자열 제거
    unique_explanations = list(set(filter(None, explanations)))

    # Step 2: GPT로 검증 요청
    gpt_response = verify_explanation_with_gpt(
        query, matched_texts, unique_explanations
    )

    return gpt_response


def verify_explanation_with_gpt(query, matched_texts, explanations):
    """
    GPT에게 문법 오류 설명 검증 및 최종 답변 생성을 요청합니다.
    """
    # GPT에 보낼 프롬프트 구성
    prompt = (
        f'사용자가 제공한 문장: "{query}"\n\n'
        "다음은 검색된 유사 문장과 각각의 문법 오류 설명입니다:\n"
    )

    for i, (text, explanation) in enumerate(zip(matched_texts, explanations), start=1):
        prompt += f'{i}. 유사 문장: "{text}"\n   설명: {explanation}\n'

    prompt += (
        "\n위 설명들이 제공된 문장에 적합한지 검토하고, 잘못된 설명이 있으면 수정하거나 제거하고,"
        " 정확한 설명만 남기세요. 문장의 형식을 유지하며 필요한 문법 오류만 수정해 주세요. "
        "의문문으로 바꾸지 말고, 평서문의 형식을 유지해야 합니다.\n"
        "결과는 다음과 같은 형식으로 제공하세요:\n"
        "Corrected Sentence: <수정된 문장>\n"
        "Explanation: <문법 오류>\n"
    )

    # GPT 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.7,
    )

    # GPT의 응답 파싱
    gpt_output = response.choices[0].message["content"].strip()

    # 수정된 문장과 설명을 각각 추출
    corrected_sentence = extract_corrected_sentence(gpt_output)
    explanation = extract_explanation(gpt_output)

    # 최종 응답 구성
    final_response = {
        "question": query,
        "corrected_sentence": corrected_sentence,
        "explanation": explanation,
    }

    return final_response


def extract_corrected_sentence(gpt_output):
    """
    GPT의 출력에서 정확한 수정된 문장만을 추출합니다.
    """
    # 'Corrected Sentence:' 이후의 텍스트 추출
    if "Corrected Sentence:" in gpt_output:
        start = gpt_output.find("Corrected Sentence:") + len("Corrected Sentence:")
        end = gpt_output.find("\n", start)
        return gpt_output[start:end].strip()

    # 다른 방법으로 패턴이 식별되지 않을 때 전체 텍스트 반환
    return gpt_output


def extract_explanation(gpt_output):
    """
    GPT의 출력에서 문법 오류 설명만을 추출합니다.
    """
    # 'Explanation:' 이후의 텍스트 추출
    if "Explanation:" in gpt_output:
        start = gpt_output.find("Explanation:") + len("Explanation:")
        return gpt_output[start:].strip()

    # 다른 방법으로 패턴이 식별되지 않을 때 빈 문자열 반환
    return ""


class GenerateAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_question = request.data.get("question", "")

        if not user_question:
            return Response(
                {"error": "질문이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Pinecone에서 관련 문서 검색 후 GPT 검증 수행
        final_response = retrieve_and_correct_with_gpt_verification(user_question)
        response_data = {
            "question": user_question,
            "answer": final_response.get("corrected_sentence", ""),
            "explanation": final_response.get("explanation", ""),   
        }

        return Response(response_data, status=status.HTTP_200_OK)


# class GenerateAnswerAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user_question = request.data.get("question", "")

#         if not user_question:
#             return Response(
#                 {"error": "질문이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
#             )

#         # Pinecone에서 관련 문서 검색
#         similar_texts, explanations = retrieve_similar_documents(user_question)
#         context = "\n".join(similar_texts)
#         explanation = ", ".join(explanations)

#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {
#                         "role": "user",
#                         "content": f"Based on the following context, correct the sentence without changing its form:\n\nContext:\n{context}\n\nSentence:\n{user_question}",
#                     },
#                 ],
#                 max_tokens=1000,
#             )

#             corrected_sentence = extract_corrected_sentence(
#                 response.choices[0].message["content"].strip()
#             )

#             final_response = {
#                 "question": user_question,
#                 "corrected_sentence": corrected_sentence,
#                 "explanation": explanation,
#             }

#             return Response(final_response, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


class ScriptEditAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 사용자 인증이 필요한 API로 설정

    def post(self, request):
        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            original_text = serializer.validated_data["original_text"]
            audience_level = serializer.validated_data.get(
                "audience_level", "general"
            )  # 기본값은 'general'로 설정

            # 사용자의 쿼리에 대해 유사한 문서 검색
            similar_texts = retrieve_similar_documents(original_text)
            context = "\n".join(similar_texts)  # 유사한 문서들을 하나의 컨텍스트로 결합

            # OpenAI API를 호출하여 대본 수정
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # 사용할 GPT 모델
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an assistant that provides context-aware responses for an audience at the '{audience_level}' level.",
                        },
                        {
                            "role": "user",
                            "content": f"Based on the following context, correct the script:\n\nContext:\n{context}\n\nScript:\n{original_text}",
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

# scripts/store_documents.py

import openai
import pinecone
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Pinecone 및 OpenAI 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
)
index = pinecone.Index("script-index")


def create_embedding(text):
    """
    OpenAI API를 사용하여 텍스트 임베딩 생성
    """
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


def store_documents_in_pinecone(documents):
    """
    여러 문서를 임베딩하여 Pinecone에 저장
    """
    for doc_id, text in documents.items():
        embedding = create_embedding(text)
        index.upsert(
            [(doc_id, embedding, {"text": text})]
        )  # 임베딩과 원본 텍스트를 메타데이터로 저장


# 저장할 문서들 (예제 데이터)
documents = {
    "doc1": "This is the first example document. It talks about Python programming.",
    "doc2": "This is the second example document. It discusses machine learning and data science.",
    "doc3": "This is the third example document. It explains the concepts of REST APIs and HTTP requests.",
}

# 문서 저장
store_documents_in_pinecone(documents)

# scripts/vector_db.py

import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Pinecone API 설정
api_key = os.getenv("PINECONE_API_KEY")

# Pinecone 초기화
pc = Pinecone(api_key=api_key)

# Pinecone 인덱스 설정
index_name = "script-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # 임베딩 차원 크기 (OpenAI의 text-embedding-ada-002 모델 크기)
        metric="cosine",  # 벡터 간 유사도 측정 방식
        spec=ServerlessSpec(
            cloud="aws",  # Pinecone 클라우드 환경 (예: 'aws', 'gcp')
            region="us-west-2",  # Pinecone 인덱스의 배포 지역
        ),
    )

index = pc.index(index_name)

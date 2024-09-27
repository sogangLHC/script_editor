from pinecone import Pinecone, Index
import os
import sys
import django
from dotenv import load_dotenv

# 환경 변수에서 Pinecone API 키를 로드하거나 직접 API 키 설정
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = "https://grammar-index-6j33r08.svc.aped-4627-b74a.pinecone.io"

# Pinecone 초기화
pc = Pinecone(api_key=pinecone_api_key)
index_name = "grammar-index"
index = Index(name=index_name, api_key=pinecone_api_key, host=pinecone_host)

# 모든 벡터 삭제
index.delete(delete_all=True)

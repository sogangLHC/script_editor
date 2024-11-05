import openai
import faiss
import numpy as np
import json
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 임베딩 차원 설정 (text-embedding-ada-002 모델은 1536차원)
dimension = 1536
index = faiss.IndexFlatL2(dimension)  # FAISS 인덱스 생성
metadata = []  # 메타데이터 저장 리스트

# FAISS 인덱스와 메타데이터 저장 경로 설정
output_dir = os.path.join(os.path.dirname(__file__), "modules")
os.makedirs(output_dir, exist_ok=True)  # modules 디렉터리가 없으면 생성

# 파일 경로 설정
faiss_index_path = os.path.join(output_dir, "faiss_index.index")
metadata_path = os.path.join(output_dir, "metadata.json")


def create_embedding(text):
    """
    텍스트 임베딩을 생성하여 FAISS 검색에 사용합니다.
    """
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return np.array(response["data"][0]["embedding"], dtype=np.float32)


# JSON 데이터를 사용하여 FAISS 인덱스와 메타데이터 저장
def add_json_data_to_faiss_index(json_data):
    """
    JSON 형식의 {문법 틀린 부분, 수정본} 데이터를 사용하여 FAISS 인덱스에 추가하고, 메타데이터와 함께 저장합니다.
    """
    embeddings = []
    for entry in json_data:
        incorrect_text = entry["incorrect"]
        corrected_text = entry["corrected"]

        # 문법 틀린 부분을 임베딩하여 인덱스에 추가
        embedding = create_embedding(incorrect_text)
        embeddings.append(embedding)
        metadata.append({"incorrect": incorrect_text, "corrected": corrected_text})

    embeddings = np.array(embeddings)
    index.add(embeddings)


# JSON 데이터 예시
json_data = [
    {"incorrect": "She go ", "corrected": "She goes "},
    {"incorrect": "He do not ", "corrected": "He does not "},
    {"incorrect": "They is ", "corrected": "They are "},
    {"incorrect": "I has ", "corrected": "I have "},
    {"incorrect": "We is ", "corrected": "We are "},
    {"incorrect": "You was ", "corrected": "You were "},
    {"incorrect": "He have ", "corrected": "He has "},
    {"incorrect": "She were ", "corrected": "She was "},
    {"incorrect": "They has ", "corrected": "They have "},
    {"incorrect": "It do ", "corrected": "It does "},
    {"incorrect": "We was ", "corrected": "We were "},
    {"incorrect": "I is ", "corrected": "I am "},
    {"incorrect": "He go ", "corrected": "He goes "},
    {"incorrect": "She do ", "corrected": "She does "},
    {"incorrect": "They was ", "corrected": "They were "},
    {"incorrect": "We has ", "corrected": "We have "},
    {"incorrect": "It were ", "corrected": "It was "},
    {"incorrect": "He are ", "corrected": "He is "},
    {"incorrect": "She have ", "corrected": "She has "},
    {"incorrect": "They do not ", "corrected": "They does not "},
    {"incorrect": "I was ", "corrected": "I were "},
    {"incorrect": "They goes ", "corrected": "They go "},
    {"incorrect": "We goes ", "corrected": "We go "},
    {"incorrect": "It are ", "corrected": "It is "},
    {"incorrect": "He were ", "corrected": "He was "},
    {"incorrect": "She am ", "corrected": "She is "},
    {"incorrect": "They do ", "corrected": "They does "},
    {"incorrect": "We does not ", "corrected": "We do not "},
    {"incorrect": "You is ", "corrected": "You are "},
    {"incorrect": "It have ", "corrected": "It has "},
]
# JSON 데이터를 사용하여 인덱스 추가 및 저장
add_json_data_to_faiss_index(json_data)

# FAISS 인덱스와 메타데이터를 파일로 저장
faiss.write_index(
    index, faiss_index_path
)  # FAISS 인덱스를 modules/faiss_index.index 파일로 저장
with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)

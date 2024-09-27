# scripts/add_grammar_data.py

import os
import sys
import django
from dotenv import load_dotenv

# Django 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 환경 변수 로드
load_dotenv()

# Django 프로젝트 설정 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "script_editor.settings")
django.setup()

import openai
from pinecone import Pinecone, Index, ServerlessSpec  # ServerlessSpec 임포트 추가
from scripts.models import GrammarRule, ExampleSentence

# OpenAI 및 Pinecone API 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = "https://grammar-index-6j33r08.svc.aped-4627-b74a.pinecone.io"  # Pinecone 인스턴스의 호스트 주소

# Pinecone 초기화
pc = Pinecone(api_key=pinecone_api_key)
index_name = "grammar-index"

# Pinecone 인덱스 생성
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI 임베딩 크기에 맞게 설정
        metric="cosine",  # 벡터 간 유사도 측정 방식
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),  # ServerlessSpec 사용
    )

index = Index(name=index_name, api_key=pinecone_api_key, host=pinecone_host)


def create_embedding(text):
    """
    OpenAI API를 사용하여 텍스트 임베딩 생성
    """
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


# 문법 규칙과 예문 데이터 1
# grammar_data = [
#     {
#         "tag": "Subject-Verb Agreement",
#         "설명": "주어와 동사의 수일치 문제",
#         "오류_예문_목록": [
#             {"문장": "He go to school.", "수정": "He goes to school."},
#             {"문장": "She play soccer.", "수정": "She plays soccer."},
#             {"문장": "The dogs barks loudly.", "수정": "The dogs bark loudly."},
#             {"문장": "My friend like pizza.", "수정": "My friend likes pizza."},
#             {"문장": "They is coming soon.", "수정": "They are coming soon."},
#         ],
#     },
#     {
#         "tag": "Article Usage Errors",
#         "설명": "관사 사용 오류",
#         "오류_예문_목록": [
#             {"문장": "I saw movie yesterday.", "수정": "I saw a movie yesterday."},
#             {"문장": "She is an best player.", "수정": "She is the best player."},
#             {"문장": "He wants a apple.", "수정": "He wants an apple."},
#             {"문장": "I have the car.", "수정": "I have a car."},
#             {"문장": "They went to an park.", "수정": "They went to a park."},
#         ],
#     },
#     {
#         "tag": "Preposition Usage Errors",
#         "설명": "전치사 사용 오류",
#         "오류_예문_목록": [
#             {"문장": "She is good in math.", "수정": "She is good at math."},
#             {
#                 "문장": "I will meet you on Monday.",
#                 "수정": "I will meet you at Monday.",
#             },
#             {
#                 "문장": "He is interested on music.",
#                 "수정": "He is interested in music.",
#             },
#             {
#                 "문장": "She walked on the street.",
#                 "수정": "She walked down the street.",
#             },
#             {"문장": "I agree on your point.", "수정": "I agree with your point."},
#         ],
#     },
#     {
#         "tag": "Tense Errors",
#         "설명": "시제 오류",
#         "오류_예문_목록": [
#             {"문장": "She has eat breakfast.", "수정": "She has eaten breakfast."},
#             {
#                 "문장": "They goes to school yesterday.",
#                 "수정": "They went to school yesterday.",
#             },
#             {
#                 "문장": "I am working here since two years.",
#                 "수정": "I have been working here for two years.",
#             },
#             {"문장": "He do it tomorrow.", "수정": "He will do it tomorrow."},
#             {"문장": "She was plays tennis.", "수정": "She was playing tennis."},
#         ],
#     },
#     {
#         "tag": "Pluralization Errors",
#         "설명": "복수형 사용 오류",
#         "오류_예문_목록": [
#             {
#                 "문장": "There are many cat in the house.",
#                 "수정": "There are many cats in the house.",
#             },
#             {"문장": "She has three childs.", "수정": "She has three children."},
#             {
#                 "문장": "The informations are useful.",
#                 "수정": "The information is useful.",
#             },
#             {"문장": "He has two foot.", "수정": "He has two feet."},
#             {"문장": "The sheeps are grazing.", "수정": "The sheep are grazing."},
#         ],
#     },
#     {
#         "tag": "Capitalization Errors",
#         "설명": "대문자 사용 오류",
#         "오류_예문_목록": [
#             {"문장": "i like to play football.", "수정": "I like to play football."},
#             {
#                 "문장": "she went to london last summer.",
#                 "수정": "She went to London last summer.",
#             },
#             {"문장": "my Birthday is in April.", "수정": "My birthday is in April."},
#             {
#                 "문장": "they visited the eiffel tower.",
#                 "수정": "They visited the Eiffel Tower.",
#             },
#             {
#                 "문장": "james Bond is a secret agent.",
#                 "수정": "James Bond is a secret agent.",
#             },
#         ],
#     },
#     # 추가 규칙과 예문들을 여기에 추가...
# ]

# 문법 규칙과 예문 데이터 2
grammar_data = [
    {
        "tag": "Subject-Verb Agreement",
        "설명": "주어와 동사의 수일치 문제",
        "오류_예문_목록": [
            {
                "문장": "She go to the market every day.",
                "수정": "She goes to the market every day.",
            },
            {
                "문장": "The team are winning the game.",
                "수정": "The team is winning the game.",
            },
            {
                "문장": "John and his friends plays soccer.",
                "수정": "John and his friends play soccer.",
            },
            {"문장": "The cat chase the mouse.", "수정": "The cat chases the mouse."},
            {"문장": "Each student have a book.", "수정": "Each student has a book."},
            {
                "문장": "The dogs barks at strangers.",
                "수정": "The dogs bark at strangers.",
            },
            {
                "문장": "The committee have decided.",
                "수정": "The committee has decided.",
            },
            {
                "문장": "One of the girls are missing.",
                "수정": "One of the girls is missing.",
            },
            {"문장": "Everybody want to join.", "수정": "Everybody wants to join."},
            {"문장": "The news are interesting.", "수정": "The news is interesting."},
        ],
    },
    {
        "tag": "Article Usage Errors",
        "설명": "관사 사용 오류",
        "오류_예문_목록": [
            {"문장": "He gave me advice.", "수정": "He gave me an advice."},
            {"문장": "She is a artist.", "수정": "She is an artist."},
            {"문장": "I have idea.", "수정": "I have an idea."},
            {"문장": "We need help.", "수정": "We need a help."},
            {
                "문장": "He bought an apple from market.",
                "수정": "He bought an apple from the market.",
            },
            {"문장": "They are playing game.", "수정": "They are playing a game."},
            {"문장": "She needs uniform.", "수정": "She needs a uniform."},
            {"문장": "There is car outside.", "수정": "There is a car outside."},
            {
                "문장": "I am reading interesting book.",
                "수정": "I am reading an interesting book.",
            },
            {"문장": "She wants answer.", "수정": "She wants an answer."},
        ],
    },
    {
        "tag": "Preposition Usage Errors",
        "설명": "전치사 사용 오류",
        "오류_예문_목록": [
            {"문장": "He is afraid from dogs.", "수정": "He is afraid of dogs."},
            {
                "문장": "She is interested at music.",
                "수정": "She is interested in music.",
            },
            {
                "문장": "He depends in his parents.",
                "수정": "He depends on his parents.",
            },
            {"문장": "They went in a walk.", "수정": "They went for a walk."},
            {
                "문장": "She will arrive on next Monday.",
                "수정": "She will arrive next Monday.",
            },
            {
                "문장": "He is good in playing piano.",
                "수정": "He is good at playing piano.",
            },
            {
                "문장": "I will wait you in the station.",
                "수정": "I will wait for you at the station.",
            },
            {
                "문장": "She is married with a lawyer.",
                "수정": "She is married to a lawyer.",
            },
            {
                "문장": "He walked in the corner.",
                "수정": "He walked around the corner.",
            },
            {
                "문장": "We agree to your proposal.",
                "수정": "We agree with your proposal.",
            },
        ],
    },
    {
        "tag": "Tense Errors",
        "설명": "시제 오류",
        "오류_예문_목록": [
            {"문장": "I am knowing the answer.", "수정": "I know the answer."},
            {"문장": "She has been arrived.", "수정": "She has arrived."},
            {"문장": "He is play tennis now.", "수정": "He is playing tennis now."},
            {
                "문장": "They have went to the park.",
                "수정": "They have gone to the park.",
            },
            {"문장": "I did not saw him.", "수정": "I did not see him."},
            {"문장": "We was eating dinner.", "수정": "We were eating dinner."},
            {
                "문장": "He is knowing her for years.",
                "수정": "He has known her for years.",
            },
            {
                "문장": "She works there since 2015.",
                "수정": "She has worked there since 2015.",
            },
            {"문장": "He will went to the party.", "수정": "He will go to the party."},
            {
                "문장": "They are finished the task.",
                "수정": "They have finished the task.",
            },
        ],
    },
    {
        "tag": "Pluralization Errors",
        "설명": "복수형 사용 오류",
        "오류_예문_목록": [
            {"문장": "I have two brother.", "수정": "I have two brothers."},
            {"문장": "She found three foxs.", "수정": "She found three foxes."},
            {
                "문장": "There are many book on the table.",
                "수정": "There are many books on the table.",
            },
            {"문장": "He has many informations.", "수정": "He has much information."},
            {"문장": "We need more equipments.", "수정": "We need more equipment."},
            {"문장": "She gave me advices.", "수정": "She gave me advice."},
            {"문장": "The childs are playing.", "수정": "The children are playing."},
            {
                "문장": "There are two mans outside.",
                "수정": "There are two men outside.",
            },
            {"문장": "She has many foots.", "수정": "She has many feet."},
            {"문장": "The sheeps are grazing.", "수정": "The sheep are grazing."},
        ],
    },
    {
        "tag": "Capitalization Errors",
        "설명": "대문자 사용 오류",
        "오류_예문_목록": [
            {"문장": "he likes to read books.", "수정": "He likes to read books."},
            {
                "문장": "january is my favorite month.",
                "수정": "January is my favorite month.",
            },
            {
                "문장": "the Eiffel tower is in paris.",
                "수정": "The Eiffel Tower is in Paris.",
            },
            {"문장": "john went to new york.", "수정": "John went to New York."},
            {"문장": "i will visit the museum.", "수정": "I will visit the museum."},
            {"문장": "they live in london.", "수정": "They live in London."},
            {
                "문장": "we celebrate christmas every year.",
                "수정": "We celebrate Christmas every year.",
            },
            {"문장": "she works at google.", "수정": "She works at Google."},
            {
                "문장": "the sun rises in the east.",
                "수정": "The sun rises in the East.",
            },
            {
                "문장": "he is a doctor at mercy hospital.",
                "수정": "He is a doctor at Mercy Hospital.",
            },
        ],
    },
]
# 데이터베이스 및 Pinecone에 저장
for rule_data in grammar_data:
    rule, created = GrammarRule.objects.get_or_create(
        tag=rule_data["tag"], description=rule_data["설명"]
    )

    for example in rule_data["오류_예문_목록"]:
        # Django 데이터베이스에 예문 저장
        example_instance = ExampleSentence.objects.create(
            rule=rule,
            incorrect_sentence=example["문장"],
            corrected_sentence=example["수정"],
        )

        # OpenAI를 사용해 임베딩 생성
        embedding = create_embedding(example["문장"])

        # Pinecone에 임베딩 저장 (설명 필드 포함)
        index.upsert(
            [
                (
                    str(example_instance.id),
                    embedding,
                    {"text": example["문장"], "explanation": rule_data["설명"]},
                )
            ]
        )

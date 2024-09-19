import requests
import dotenv
import os
import json

dotenv.load_dotenv() # .env에서 환경 변수 로드하기

SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
SEARCH_ENGINE_API_KEY = os.getenv('SEARCH_ENGINE_API_KEY')
search_query = "subject and verb agreement"
CUSTOM_SEARCH_ENGINE_URI = f"https://www.googleapis.com/customsearch/v1?key={SEARCH_ENGINE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"

#response = requests.get(CUSTOM_SEARCH_ENGINE_URI).json() // 검색 결과 모두 받아오기
#print(response)

f = open('data.json')
search_result = json.load(f)

print(search_result['items'])

for i in search_result['items']:
    print(i['title'], i['link'])
import requests
import dotenv
import os
import json

dotenv.load_dotenv() # .env에서 환경 변수 로드하기

SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
SEARCH_ENGINE_API_KEY = os.getenv('SEARCH_ENGINE_API_KEY')
search_query = "past tense"  # 쿼리 개선 기능으로 보완해도 됨.
CUSTOM_SEARCH_ENGINE_URI = f"https://www.googleapis.com/customsearch/v1?key={SEARCH_ENGINE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"

data = requests.get(CUSTOM_SEARCH_ENGINE_URI).json() # 검색 결과 모두 받아오기
#print(response)

# Test JSON file
#f = open('data.json')
#data = json.load(f)

top10_search_results = []

for i in range(len(data['items'])):
    title = data['items'][i]['title']
    link = data['items'][i]['link']
    top10_search_results.append({"result_index": i, "title": title, "link": link})

print(top10_search_results)
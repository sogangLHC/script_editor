import requests, pprint

# LanguageTool API endpoint
url = "https://api.languagetool.org/v2/check"

# 테스트할 문장
text = "The people who are tall is nice."

# API 요청에 필요한 데이터
data = {
    'text': text,
    'language': 'en',  # 언어 설정
}

# API 요청 보내기
response = requests.post(url, data=data)
result = response.json()

# 원본 텍스트를 수정한 새로운 텍스트
corrected_text = text
offset_adjustment = 0  # 위치 오차 조정 변수

# 오류가 있을 경우
if result['matches']:
    for match in result['matches']:
        # 교정 제안이 있을 경우 첫 번째 제안을 사용
        if match['replacements']:
            start = match['offset'] + offset_adjustment
            end = start + match['length']
            replacement = match['replacements'][0]['value']
            
            # 수정된 텍스트 생성
            corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
            
            # 교정된 길이 차이만큼 오차 조정
            offset_adjustment += len(replacement) - match['length']

    print("수정된 문장:", corrected_text)
else:
    print("문법 오류가 발견되지 않았습니다.")


pprint(result)
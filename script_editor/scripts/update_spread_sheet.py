"""
    grammar_data.json 파일의 내용을 Google Spread Sheet에 POST하는 스크립트.
"""

import requests
import json


def camel_case(s):
    words = s.replace("-", " ").split()
    camel_cased = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_cased


SHEET_TAGS = {
    "Subject-Verb Agreement": "주어와 동사의 수일치 문제",
    "Article Usage Errors": "관사 사용 오류",
    "Preposition Usage Errors": "전치사 사용 오류",
    "Tense Errors": "시제 오류",
    "Pluralization Errors": "복수형 사용 오류",
    "Capitalization Errors": "대문자 사용 오류",
}

# JSON 파일 읽기
with open("grammar_data.json", "r", encoding='utf-8') as f:
    grammar_data = json.load(f)


class WrongSentenceSheet:

    def create_sheety_end_point(self, tag_):
        tag_ = camel_case(tag_)
        sheety_end_point = f"https://api.sheety.co/ecdda9522fa86a7eb2b459b27d6bec30/lhcWrongSentenceData/{tag_}"
        return sheety_end_point

    def update_sheet(self):
        for data in grammar_data:
            print(data)
            tag = camel_case(data['tag'])
            if tag[len(tag) - 1] == "s":
                tag = tag[:len(tag) - 1]

            # 현재 문장 단위로 Sheet를 작성하고 있어서 request 요청이 과도함. Sheety가 지원하는 방식을 다시 확인할 필요 있음.
            for sentence in data["오류_예문_목록"]:

                input_data = {
                    tag: {
                        "문장": sentence["문장"],
                        "수정": sentence["수정"],
                    }
                }

                # SHEETY API POST 요청
                try:
                    post_response = requests.post(url=self.create_sheety_end_point(data['tag']), json=input_data)

                    # 응답 상태 확인
                    if post_response.status_code == 200:
                        print(f"Updated successfully for tag: {data['tag']}")
                    else:
                        print(f"Failed to update for tag: {data['tag']} - Status Code: {post_response.status_code}")
                        print(f"Response: {post_response.json()}")  # 실패 시 응답 내용 출력
                except Exception as e:
                    print(f"An error occurred while updating tag: {data['tag']} - Error: {str(e)}")


if __name__ == "__main__":
    inst = WrongSentenceSheet()
    inst.update_sheet()

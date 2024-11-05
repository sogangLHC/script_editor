"""
    Google Spread Sheet에 저장된 영어 비문과 수정된 문장을 json 파일로 변환하는 스크립트.
    해당 json 데이터는 RAG를 위한 embeding 대상임.
"""

import requests
import json


# 문자열 s를 Camel Case로 변환
def camel_case(s):
    words = s.replace("-", " ").split()
    camel_cased = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_cased


"""
    최종 json 파일에 담길 데이터
    {
        "tag": "",
        "설명": "",
        "오류_예문_목록": [],
    } 를 저장하는 list.
"""
GRAMMAR_DATA = []

# 문법 오류 tag: 설명(틀린 이유) -> 조금 더 구체화 & 세분화 되면 별도의 파일로 분리하기
SHEET_TAGS = {
    "Subject-Verb Agreement": "주어와 동사의 수일치 문제",
    "Article Usage Errors": "관사 사용 오류",
    "Preposition Usage Errors": "전치사 사용 오류",
    "Tense Errors": "시제 오류",
    "Pluralization Errors": "복수형 사용 오류",
    "Capitalization Errors": "대문자 사용 오류",
}


class WrongSentenceJson:
    """
    Google Spread Sheet의 비문 데이터를 JSON 형식으로 변환
    """

    def __init__(self):
        self.sheet_data = []  # 각 시트 상의 데이터
        self.data_per_error_type = []  # Error_type 별 데이터

    def create_sheety_end_point(self, tag_):
        """
        Sheety(스프레드 시트  CRUD API) endpoint 생성
        """
        tag_ = camel_case(tag_)
        sheety_end_point = f"https://api.sheety.co/ecdda9522fa86a7eb2b459b27d6bec30/lhcWrongSentenceData/{tag_}"
        return sheety_end_point

    def create_json(self):
        """
        1. 비문 유형에 따라 분류된 각 시트를 순회하면서 해당 비문 유형에 관한 오류 예문 목록 ({문장"(비문): "수정"(정정된 문장)}) 데이터를 저장.
        2. 현재 디렉토리에 "grammar_data.json"을 생성함.
        """
        for tag, explanation in SHEET_TAGS.items():
            try:
                get_response = requests.get(self.create_sheety_end_point(tag))  # GET Request

                if get_response.status_code == 200:
                    print(f"Collected data successfully for tag: {tag}")
                    sheet_data = get_response.json()[camel_case(tag)]  # 오류_예문_목록의 element.
                    data_per_error_type = {
                        "tag": tag,
                        "설명": explanation,
                        "오류_예문_목록": []
                    }
                    for i in range(len(sheet_data)):
                        sentence_data = {
                            "문장": sheet_data[i]["문장"],
                            "수정": sheet_data[i]["수정"],
                        }
                        data_per_error_type['오류_예문_목록'].append(sentence_data)  # 시트에 저장된 비문과 올바른 문장을 list에 저장.

                    GRAMMAR_DATA.append(data_per_error_type)

                    with open("grammar_data.json", "w", encoding="utf-8") as f:  # "grammar_data".json file 생성
                        json.dump(GRAMMAR_DATA, f, ensure_ascii=False, indent=4)
                else:
                    print(f"Failed to update for tag: {tag} - Status Code: {get_response.status_code}")
                    print(f"Response: {get_response.json()}")  # 실패 시 응답 내용 출력
            except Exception as e:
                print(f"An error occurred while updating tag: {tag} - Error: {str(e)}")


if __name__ == "__main__":
    inst = WrongSentenceJson()
    inst.create_json()

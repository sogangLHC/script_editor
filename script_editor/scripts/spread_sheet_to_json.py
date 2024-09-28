import requests
import json


def camel_case(s):
    words = s.replace("-", " ").split()
    camel_cased = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_cased


GRAMMAR_DATA = []

SHEET_TAGS = {
    "Subject-Verb Agreement": "주어와 동사의 수일치 문제",
    "Article Usage Errors": "관사 사용 오류",
    "Preposition Usage Errors": "전치사 사용 오류",
    "Tense Errors": "시제 오류",
    "Pluralization Errors": "복수형 사용 오류",
    "Capitalization Errors": "대문자 사용 오류",
}


class WrongSentenceJson:
    def __init__(self):
        self.sheet_data = []
        self.data_per_error_type = []

    def create_sheety_end_point(self, tag_):
        tag_ = camel_case(tag_)
        sheety_end_point = f"https://api.sheety.co/ecdda9522fa86a7eb2b459b27d6bec30/lhcWrongSentenceData/{tag_}"
        return sheety_end_point

    def create_json(self):
        for tag, explanation in SHEET_TAGS.items():
            sheet_data = requests.get(self.create_sheety_end_point(tag)).json()[
                camel_case(tag)]  # tag별 틀린 문장, 수정된 문장의 List. List의 각 Element는 dict.
            data_per_error_type = {
                "tag": tag,
                "설명": explanation,
                "오류_예문_목록": []
            }

            for i in range(len(sheet_data)):
                sentence_data = {
                    "문장": sheet_data[i]['문장'],
                    "수정": sheet_data[i]['수정'],
                }
                data_per_error_type['오류_예문_목록'].append(sentence_data)

            GRAMMAR_DATA.append(data_per_error_type)

        with open("grammar_data.json", "w", encoding="utf-8") as f:
            json.dump(GRAMMAR_DATA, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    inst = WrongSentenceJson()
    inst.create_json()

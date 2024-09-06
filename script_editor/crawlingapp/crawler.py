import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


#Constants
SEARCH_ENGINE = {
    "google": {"url": "https://www.google.com",
               "search_bar_XPATH": '//*[@id="APjFqb"]',
               },

    "youtube": {"url": "https://www.youtube.com",
                "search_bar_XPATH": '//*[@id="search"]',
                }
    }
ERROR_TYPE = ["wrong grammar", "ambiguity", "context"]  # 오류 타입 정의 -> 문법(형태론), 중의성(의미론), 맥락(화용론)

# Chrome Driver Set Up
options = Options()
options.add_experimental_option("detach", True)  # 프로세스 종료 후 브라우저가 닫히지 않도록 함.


# Selenium -> 선택한 검색 엔진 (google 또는 youtube)에 대해서 검색을 수행하는 클래스
class Searcher:
    def __init__(self, error_type, error_keyword):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.error_type = error_type
        self.error_keyword = error_keyword

    # 쿼리 보완 필요. 항상 원하는 결과물을 얻을 수 없음.
    def create_search_query(self, search_engine):
        """ Search Query 생성

        Positional Arguments:
        search_engine -- default: 'google'
        """
        search_engine = 'google'
        primary_reference = None
        if search_engine == 'google':
            primary_reference = 'https://www.ox.ac.uk/'
        elif search_engine == 'youtube':
            primary_reference = 'university lecture'
        query = f"{self.error_keyword} {self.error_type} site:{primary_reference}"

        return query

    def search_on(self, search_engine):
        """ 생성된 search query를 이용해 선택한 검색 엔진에서 검색을 수행하는 함수

        Positional Arguments:
        search_engine -- default: 'google
        """
        self.driver.get(SEARCH_ENGINE[search_engine]["url"])
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)
        search_bar = self.driver.find_element(by=By.XPATH, value=SEARCH_ENGINE[search_engine]["search_bar_XPATH"])
        search_query = self.create_search_query(search_engine)
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(2)

    def terminate_searcher(self):
        """ Selenium driver 종료 """
        self.driver.quit()


""" 구현 예정 """
# 검색 결과 웹 페이지로부터 상위 n개의 URL Reference Crawling을 수행하는 클래스
class Crawler:
    def __init__(self, error_type, source_url):
        self.soup = BeautifulSoup(source_url, )

    def run(self):
        return


# For test
""" Youtube에서 검색할 때 에러 뜸. """
if __name__ == '__main__':
    searcher = Searcher(ERROR_TYPE[0], "ambiguous word use")
    searcher.search_on('google')
    #searcher.terminate_searcher()
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import lxml  # Parser

# Constants
SEARCH_ENGINE = {
    "google": {"url": "https://www.google.com",
               "search_bar_XPATH": '//*[@id="APjFqb"]',
               "primary_reference": 'https://www.ox.ac.uk/'
               },

    "youtube": {"url": "https://www.youtube.com",
                "search_bar_XPATH": '//*[@id="search"]',
                "primary_reference": 'university lecture',
                }
}
ERROR_TYPE = ["wrong grammar", "ambiguity", "context"]  # 오류 타입 정의 -> 문법(형태론), 중의성(의미론), 맥락(화용론)
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Chrome Driver Set Up
options = Options()
options.add_experimental_option("detach", True)  # 프로세스 종료 후 브라우저가 닫히지 않도록 함.


# Selenium -> 선택한 검색 엔진 (google 또는 youtube)에 대해서 검색을 수행하는 클래스
class Searcher:
    def __init__(self, error_type, error_description, search_engine):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.error_type = error_type
        self.error_description = error_description
        self.search_engine = search_engine
        self.current_url = None

    # 쿼리 보완 필요. 항상 원하는 결과물을 얻을 수 없음.
    def create_search_query(self):
        """ Search Query 생성

        Positional Arguments:
        search_engine -- default: 'google'
        """
        search_engine = 'google'
        primary_reference = SEARCH_ENGINE[self.search_engine]["primary_reference"]
        query = f"{self.error_description} {self.error_type} site:{primary_reference}"

        return query

    def search(self):
        """ 생성된 search query를 이용해 선택한 검색 엔진에서 검색을 수행하는 함수

        Positional Arguments:
        search_engine -- default: 'google
        """
        self.driver.get(SEARCH_ENGINE[self.search_engine]["url"])
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)
        search_bar = self.driver.find_element(by=By.XPATH, value=SEARCH_ENGINE[self.search_engine]["search_bar_XPATH"])
        search_query = self.create_search_query()
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(2)
        self.current_url = self.driver.current_url

        return self.current_url

    def terminate_searcher(self):
        """ Selenium driver 종료 """
        self.driver.quit()


""" 구현 예정 """


# 검색 결과 웹 페이지로부터 상위 n개의 URL Reference Crawling을 수행하는 클래스
class Crawler:
    def __init__(self, error_type, error_description, search_engine):
        self.searcher = Searcher(error_type, error_description, search_engine)
        self.current_url = self.searcher.search()
        self.target_page = requests.get(self.current_url, headers=HEADERS).text
        self.soup = BeautifulSoup(self.target_page, "lxml")
        self.reference_url = []

    def crawl_top_urls(self, count):
        titles = self.soup.find_all('cite')
        for title in titles[:6:2]:
            print(title)
        return

    def run(self):
        return


# For test
""" Youtube에서 검색할 때 에러 뜸. """
if __name__ == '__main__':
    crawler = Crawler(ERROR_TYPE[0], "ambiguous word use", 'google')
    crawler.crawl_top_urls(5)
    # searcher.terminate_searcher()

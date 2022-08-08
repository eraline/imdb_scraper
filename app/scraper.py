import time
import re
from dataclasses import dataclass
from turtle import ht
from fake_useragent import UserAgent
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def get_user_agent():
    return UserAgent(verify_ssl=False).random

@dataclass
class Scraper:
    url: str = None
    endless_scroll: bool = False
    endless_scroll_time: int = 5
    driver: WebDriver = None
    html_obj: HTML = None
    imdb_id: str = None

    def __post_init__(self):
        if self.imdb_id:
            self.url = f'https://www.imdb.com/title/{self.imdb_id}/'
        if not self.imdb_id and not self.url:
            raise Exception('Imdb_id or url is required')
            
    def get_driver(self):
        if self.driver is None:
            user_agent = get_user_agent()
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options)
            self.driver = driver
        return self.driver

    def perform_endless_scroll(self, driver):
        if self.endless_scroll:
            current_height = driver.execute_script(
                'return document.body.scrollHeight')
            while True:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(self.endless_scroll_time)
                iter_height = driver.execute_script(
                    'return document.body.scrollHeight')
                if current_height == iter_height:
                    break
                current_height = iter_height
        return 

    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get()
            self.html_obj = HTML(html=html_str) 
        return self.html_obj

    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        if self.endless_scroll:
            self.perform_endless_scroll(driver=driver)
        else:
            time.sleep(10)
        return driver.page_source

    def extract_an_element(self, html_obj, element):
        result = html_obj.find(element, first=True)
        if not result:
            return ''
        return result

    def extract_list_from_element(self, html_obj, element):
        obj = html_obj.find(element)
        results = [item.text for item in obj]
        if not results:
            return []
        return results

    def scrape(self):
        html_obj = self.get_html_obj()
        pattern = '\S*title\/(?P<imdb_id>\S*)\/\S*'
        imdb_id = re.search(pattern, self.url).group('imdb_id')
        title_str = self.extract_an_element(
            html_obj,
            "[data-testid='hero-title-block__title']").text
        year_str = self.extract_an_element(
            html_obj,
            '.sc-8c396aa2-2').text
        genres_obj = self.extract_an_element(
            html_obj,
            "[data-testid='storyline-genres']")
        genres = self.extract_list_from_element(
            genres_obj,
            '.ipc-metadata-list-item__list-content-item')
        
        return {
            'imdb_id': imdb_id,
            'year': year_str,
            'title': title_str,
            'genres': genres
        }





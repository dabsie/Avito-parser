import json

import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = option)

class AvitoParse:
    """Парсинг бесплатных товаров на avito.ru
    url - начальный url
    items - список ключевых слов
    count - сколько проверять страниц
    version_main - версия Chrome которая установлена
    """

    def __init__(self, url: str, count: int = 100):
        self.url = url
        self.count = count
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main = 117)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        """Кнопка далее"""
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']") and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count -= 1

    def __parse_page(self):
        """Парсит открытую страницу"""
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        print(f"Found {len(titles)} cards")
        for title in titles:
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            data = {
                'name': name,
                'url': url,
                'price': price
            }
            print(data)
            self.data.append(data)
        self.__save_data()

    def __save_data(self):
        """Сохраняет результат в файл items.json"""
        with open("items.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        #self.__parse_page()


if __name__ == "__main__":
    AvitoParse(
        url='https://www.avito.ru/ekaterinburg/telefony',
        count=2,
    ).parse()

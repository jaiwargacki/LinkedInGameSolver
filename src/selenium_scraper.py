from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

class Connection:
    def __init__(self, url, start_button_id, game_element_id):
        self.url = url
        self.start_button_id = start_button_id
        self.game_element_id = game_element_id
        self.driver = None

    def open(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        self.driver.get(self.url)
        time.sleep(1)
        start_button = self.driver.find_element("id", self.start_button_id)
        start_button.click()
        time.sleep(1)
        return self

    def get_game_elements(self):
        board_element = self.driver.find_element("id", self.game_element_id)
        divs = board_element.find_elements("tag name", "div")
        return enumerate(divs)

    def close(self):
        self.driver.quit()

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

START_BUTTON_ID = "launch-footer-start-button"

class Connection:
    def __init__(self, url, game_element_class):
        self.url = url
        self.game_element_class = game_element_class
        self.driver = None

    def open(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        self.driver.get(self.url)
        time.sleep(1)
        start_button = self.driver.find_element("id", START_BUTTON_ID)
        start_button.click()
        time.sleep(1)
        return self

    def get_game_elements(self):
        board_element = self.driver.find_element("class name", self.game_element_class)
        divs = board_element.find_elements("css selector", ":scope > div")
        return enumerate(divs)

    def close(self):
        self.driver.quit()

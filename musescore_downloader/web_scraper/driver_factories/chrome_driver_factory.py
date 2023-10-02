from urllib.error import URLError

import selenium
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from . import BaseDriverFactory

class ChromeDriverFactory(BaseDriverFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_driver(self):
        manager = ChromeDriverManager()

        try:
            driver_path = manager.install()
        except URLError as e:
            raise e
        
        service = ChromeService(driver_path)

        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")

        if self.headless:
            options.add_argument("--headless=new")

        return Chrome(options, service)

from urllib.error import URLError

import selenium
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from . import BaseDriverFactory

class ChromeDriverFactory(BaseDriverFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_driver(self, path=None):
        try:
            if path is not None:
                driver_path = path
            else:
                manager = ChromeDriverManager()
                driver_path = manager.install()
            service = ChromeService(driver_path)
        except URLError as e:
            raise e


        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extension")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('---incognito')

        if self.headless:
            options.add_argument("--headless=new")

        return Chrome(options, service)

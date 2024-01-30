from urllib.error import URLError

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from . import BaseDriverFactory

class FirefoxDriverFactory(BaseDriverFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_driver(self, path=None):
        options = FirefoxOptions()

        try:
            if path is not None:
                driver_path = path
            else:
                driver_path = GeckoDriverManager().install()
            
            service = FirefoxService(driver_path)
        except URLError as e:
            raise e

        
        return Firefox(None, service)
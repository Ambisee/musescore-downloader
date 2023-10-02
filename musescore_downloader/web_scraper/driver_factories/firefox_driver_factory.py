from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from . import BaseDriverFactory

class FirefoxDriverFactory(BaseDriverFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_driver(self):
        manager = GeckoDriverManager().install()

        options = FirefoxOptions()
        options.add_argument('-headless')
        options.add_argument('-devtools')

        service = FirefoxService(manager)
        
        return Firefox(options, service)
    
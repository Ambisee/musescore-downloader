import os
import logging
from urllib.error import URLError

import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    InvalidArgumentException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from webdriver_manager.chrome import ChromeDriverManager

from ..common.exceptions import (
    UninitializedWebDriverError,
    PageElementNotFoundError,
    InitialElementNotFoundError
)
from ..common.types import ScoreScraperResult
from ..managers import SelectorsManager

class ScoreScraper:
    """Scrapes the URLs that corresponds to the pages of a Musescore music sheet.

    Attributes
    ----------
    selectors_manager : SelectorsManager
        The object that contains the CSS selectors of the HTML elements that contains information.
    url : str
        The URL to the music sheet's webpage.
    timeout : float
        The time (in seconds) for the driver to wait for a certain condition to be fulfilled before timeout.
    """

    def __init__(
        self,
        selectors_manager: SelectorsManager,
        url: str | None = None,
        timeout: float = 10,
    ) -> None:
        self.selectors_manager: SelectorsManager = selectors_manager
        self.driver: webdriver.Chrome | None = None
        self.url: str | None = url
        self.timeout: float = timeout


    def set_url(self, url: str) -> None:
        self.url = url

    def set_timeout(self, timeout: float) -> None:
        self.timeout = timeout

    def initialize(
        self, 
        use_headless: bool = True,
    ) -> None:
        """Initializes the webdriver instance.
        
        Parameters
        ----------
        use_headless : bool, default=True
            Toggles the browser's headless mode.

        Returns
        -------
        None

        Raises
        ------
        URLError
            Unable to retrieve the web driver of the browser.
        """

        try:
            chrome_service = ChromeService(ChromeDriverManager().install())
        except URLError as e:
            raise e

        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--start-maximized")


        if use_headless:
            chrome_options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(chrome_options, chrome_service)

    def shutdown_driver(self):
        """Performs teardown on the currently active webdriver

        Returns
        -------
        None
        """
        self.driver.close()
        self.driver.quit()

    def find_initial_img_element(self):
        try:
            self.driver.get(self.url)
            initial_img_element: WebElement = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"{self.selectors_manager.page_container_selector} > img"))
            )
        except InvalidArgumentException as e:
            self.shutdown_driver()
            raise e
        except URLError as e:
            self.shutdown_driver()
            raise e
        except TimeoutException:
            self.shutdown_driver()
            raise InitialElementNotFoundError()
        
        return initial_img_element

    def find_page_element(self, page_containers, i):
        logging.info(f"Retrieving URL for page {i + 1}...")
        self.driver.execute_script(f"pageContainers[{i}].scrollIntoViewIfNeeded()")

        try:
            page_image_url: WebElement = WebDriverWait(self.driver, self.timeout).until(
                lambda driver: page_containers[i].find_element(By.TAG_NAME, "img").get_attribute("src")
            )
        except TimeoutException as e:
            print(e)
            self.shutdown_driver()
            raise PageElementNotFoundError()
        except URLError:
            self.shutdown_driver()
            raise URLError()
        
        return page_image_url

    def execute(self) -> ScoreScraperResult:
        """Starts the process of web scraping as specified by the class.

        Returns
        -------
        ScoreScraperResult
            Object containing the title, total number of pages, and the pages' URLs of
            the target music sheet.
        
        Raises
        ------
        UninitializedWebDriverError
            `execute` was called before the scraper was initialized.
        TypeError
            The target URL is not set.
        NoSuchElementException
            The web driver cannot find a corresponding HTML element. Possible causes: 
            - The scraper received a non-Musescore URL.
            - The scaper was given outdated CSS selectors.
            - The time to wait for the element to appear before timing out is too short.
        URLError
            The webdriver cannot connect to a web page. Possible causes:
            - The scraper received an invalid web URL.
            - The user is currently offline.
        """
        if not self.driver:
            raise UninitializedWebDriverError("Web driver is not initialized. Please initialize the scraper and set url for a music sheet on Musescore before running it.")

        if not self.url:
            raise TypeError("The target URL is not set. Please initialize the scraper and set url for a music sheet on Musescore before running it.")

        initial_img_element = self.find_initial_img_element()

        page_containers = self.driver.find_elements(By.CSS_SELECTOR, self.selectors_manager.page_container_selector)
        title = self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.title_container_selector).text
        total_pages = self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.total_pages_container_selector).text
        total_pages = int(total_pages)
    
        logging.info(f"Retrieved the title of the music sheet: {title}")
        logging.info(f"Retrieved the number of total pages in the music sheet: {total_pages} pages in total")

        self.driver.execute_script(f"scrollElement = document.querySelector('{self.selectors_manager.scroll_element_selector}')")
        self.driver.execute_script(f"pageContainers = document.querySelectorAll('{self.selectors_manager.page_container_selector}')")

        image_urls = [initial_img_element.get_attribute("src")]

        logging.info("Retrieving URL for page 1...")
        logging.info("Retrieved URL for page 1.")

        for i in range(1, total_pages):
            page_image_url = self.find_page_element(page_containers, i)

            image_urls.append(page_image_url)
            logging.info(f"Retrieved URL for page {i + 1}.")

        self.shutdown_driver()

        logging.info("The scraper has been closed. Please reinitialize the scraper before running it again.")
        logging.info("Finished retrieving image URLS for each page of the music sheet.")

        return ScoreScraperResult(
            title,
            image_urls,
            total_pages,
        )

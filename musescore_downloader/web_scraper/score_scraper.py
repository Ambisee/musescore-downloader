import sys
import logging
from urllib.error import URLError

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    InvalidArgumentException,
    NoSuchElementException
)

from ..common.exceptions import (
    UninitializedWebDriverError,
    PageElementNotFoundError,
    InitialElementNotFoundError,
    MetadataElementNotFoundError,
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
        driver,
        url: str | None = None,
        timeout: float = 10,
    ) -> None:
        self.selectors_manager: SelectorsManager = selectors_manager
        self.driver: WebDriver = driver
        self.url: str | None = url
        self.timeout: float = timeout


    def set_url(self, url: str) -> None:
        self.url = url

    def set_timeout(self, timeout: float) -> None:
        self.timeout = timeout

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
        except Exception as e:
            self.shutdown_driver()
            raise e
        
        return initial_img_element

    def try_get_page_element(self, driver, page_containers, i):
        self.driver.execute_script(
            "window.pageContainers[arguments[0]].scrollIntoView({ block: arguments[1] });", 
            i,
            "center"
        )
        return page_containers[i].find_element(By.TAG_NAME, "img").get_attribute("src")

    def find_page_element(self, page_containers, i):
        logging.info(f"Retrieving URL for page {i + 1}...")
        
        try:
            page_image_url: str = WebDriverWait(self.driver, self.timeout).until(
                lambda driver: self.try_get_page_element(driver, page_containers, i)
            )
        except TimeoutException as e:
            self.shutdown_driver()
            raise PageElementNotFoundError(i + 1)
        except URLError:
            self.shutdown_driver()
            raise URLError()
        except Exception as e:
            self.shutdown_driver()
            raise e
        
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

        page_containers, title, total_pages = self.find_metadata_elements()
        total_pages = int(total_pages)
    
        logging.info(f"Retrieved the title of the music sheet: {title}")
        logging.info(f"Retrieved the number of total pages in the music sheet: {total_pages} pages in total")

        self.driver.execute_script(f"window.scrollElement = document.querySelector(arguments[0]);", self.selectors_manager.scroll_element_selector)
        self.driver.execute_script(f"window.pageContainers = document.querySelectorAll(arguments[0]);", self.selectors_manager.page_container_selector)

        self.driver.execute_script(f"console.log(window.scrollElement);")
        self.driver.execute_script(f"console.log(scrollElement);")
        self.driver.execute_script(f"console.log(scrollElement);")
        self.driver.execute_script(f"console.log(window.pageContainers);")

        image_urls = [initial_img_element.get_attribute("src")]

        logging.info("Retrieving URL for page 1...")
        logging.info("Retrieved URL for page 1.")

        for i in range(1, total_pages):
            page_image_url = self.find_page_element(page_containers, i)

            image_urls.append(page_image_url)
            logging.info(f"Retrieved URL for page {i + 1}.")

        logging.info(self.driver.get_log('browser'))
        self.shutdown_driver()

        logging.info("The scraper has been closed. Please reinitialize the scraper before running it again.")
        logging.info("Finished retrieving image URLS for each page of the music sheet.")


        return ScoreScraperResult(
            title,
            image_urls,
            total_pages,
        )

    def find_metadata_elements(self):
        try:
            page_containers = self.driver.find_elements(By.CSS_SELECTOR, self.selectors_manager.page_container_selector)
            # title = self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.title_container_selector).text
            # total_pages = self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.total_pages_container_selector).text
            
            title = WebDriverWait(self.driver, self.timeout).until(
                lambda driver: self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.title_container_selector).text
            )

            total_pages = WebDriverWait(self.driver, self.timeout).until(
                lambda driver: self.driver.find_element(By.CSS_SELECTOR, self.selectors_manager.total_pages_container_selector).text
            )
        except NoSuchElementException as e:
            raise PageElementNotFoundError()
        except TimeoutException as e:
            raise MetadataElementNotFoundError(e)
        
        return page_containers, title, total_pages
        
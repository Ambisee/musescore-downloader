import logging

import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from get_chrome_driver import GetChromeDriver

from ..common.types.score_scraper_result import ScoreScraperResult

class UninitializedWebDriverError(Exception):
    """No webdriver initialized."""

class ScoreScraper:
    """Scrapes the URLs that corresponds to the pages of a Musescore music sheet.

    Attributes
    ----------
    scroll_element_selector : str
        The CSS selector that targets the scrollable container that contains the sheet's pages.
    page_container_selector : str
        The CSS selector that targets the container element that contains the pages.
    total_pages_container_selector : str
        The CSS selector that targets the element containing the total number of pages in the music sheet.
    title_container_selector : str
        The CSS selector that targets the element containing the title of the music sheet.
    url : str
        The URL to the music sheet's webpage.
    timeout : float
        The time (in seconds) for the driver to wait for a certain condition to be fulfilled before timeout.
    """

    def __init__(
        self,
        scroll_element_selector: str,
        page_container_selector: str,
        total_pages_container_selector: str,
        title_container_selector: str,
        url: str | None = None,
        timeout: float = 10,
    ):
        self.scroll_element_selector = scroll_element_selector
        self.page_container_selector = page_container_selector
        self.total_pages_container_selector = total_pages_container_selector
        self.title_container_selector = title_container_selector

        self.driver: webdriver.Chrome | None = None
        self.url: str | None = url
        self.timeout: float = timeout

    def set_url(self, url: str):
        self.url = url

    def set_timeout(self, timeout: float):
        self.timeout = timeout

    def initialize(
        self, 
        use_headless: bool=True,
        window_size: None | tuple[int, int] | list[int, int]=None,
    ):
        """Initializes the webdriver instance.
        
        Parameters
        ----------
        use_headless : bool, default=True
            Toggles the browser's headless mode.
        window_size : list or tuple of int, default=None
            Specifies the window size of the initialized browser. The list or tuple must
            have exactly two elements which represents the width and the height of the window respectively. 
            Default value is `None` which tells the webdriver to use a window size of `1280x1080`.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            `window_size` is neither of type None nor list or tuple of ints.
        ValueError
            `window_size
        """
        get_driver = GetChromeDriver()
        get_driver.install()

        options = ChromeOptions()

        if window_size is not None:
            if not isinstance(window_size, (list, tuple)): 
                raise TypeError(f"Expected `window_size` to be an instance of list or tuple, {type(window_size)} found.")
            if len(window_size) != 2:
                raise ValueError(f"Expected `window_size` to be a list or tuple of length 2, found list or tuple of length {len(window_size)}.")
            
            options.add_argument(f"---window-size={window_size[0]},{window_size[1]}")
        else:
            options.add_argument("--window-size=1280,1080")

        if use_headless:
            options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options)

    def execute(self):
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
            - The scraper received an invalid Musescore URL.
            - The scaper was given outdated CSS selectors.
            - The time to wait for the element to appear before timing out is too short.
        """

        if not self.driver:
            raise UninitializedWebDriverError("Web driver is not initialized. Please initialize the scraper and set url for a music sheet on Musescore before running it.")
        
        if not self.url:
            raise TypeError("The target URL is not set. Please initialize the scraper and set url for a music sheet on Musescore before running it.")
        
        try:
            self.driver.get(self.url)
            initial_img_element:WebElement = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"{self.page_container_selector} > img"))
            )
        except TimeoutException:
            self.driver.close()
            self.driver.quit()

            raise NoSuchElementException("The initial page of the music sheet is not found. Please ensure that you have set the correct Musescore URL.")

        page_containers = self.driver.find_elements(By.CSS_SELECTOR, self.page_container_selector)
        title = self.driver.find_element(By.CSS_SELECTOR, self.title_container_selector).text
        total_pages = self.driver.find_element(By.CSS_SELECTOR, self.total_pages_container_selector).text
        total_pages = int(total_pages)
    
        logging.info(f"Retrieved the title of the music sheet: {title}")
        logging.info(f"Retrieved the number of total pages in the music sheet: {total_pages} pages in total")

        self.driver.execute_script(f"scrollElement = document.querySelector('{self.scroll_element_selector}')")
        self.driver.execute_script(f"pageContainers = document.querySelectorAll('{self.page_container_selector}')")

        image_urls = [initial_img_element.get_attribute("src")]

        logging.info("Retrieving URL for page 1...")
        logging.info("Retrieved URL for page 1.")
        for i in range(1, total_pages):
            logging.info(f"Retrieving URL for page {i + 1}...")
            self.driver.execute_script(f"pageContainers[{i}].scrollIntoViewIfNeeded()")

            try:
                page_image_url: WebElement = WebDriverWait(self.driver, self.timeout).until(
                    lambda driver: page_containers[i].find_element(By.TAG_NAME, "img").get_attribute("src")
                )
            except TimeoutException:
                self.driver.close()
                self.driver.quit()

                raise NoSuchElementException("The next page cannot be found. The operation will be terminated. Please reinitialize the scraper and try again.")
            
            image_urls.append(page_image_url)
            logging.info(f"Retrieved URL for page {i + 1}.")

        self.driver.close()
        self.driver.quit()

        logging.info("The scraper has been closed. Please reinitialize the scraper before running it again.")
        logging.info("Finished retrieving image URLS for each page of the music sheet.")

        return ScoreScraperResult(
            title,
            image_urls,
            total_pages,
        )

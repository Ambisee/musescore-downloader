import logging
from concurrent.futures import (
    ThreadPoolExecutor, 
    Future,
    wait
)

import requests
from requests import RequestException

from ..common.types.content_object import ContentObject

class PageFileScraper:
    """Scrapes the image data from a given list of page URLs.
    
    Attributes
    ----------
    title : str
        The title of the music sheet.
    urls : list or tuple of str
        The URLs that corresponds to the image data of each page
        of the music sheet. The URLs' position will correspond to the page number
        of the data it possesses in the music sheet.
    """

    def __init__(self, urls, title):
        self.urls = urls
        self.title = title

    def set_urls(self, urls):
        self.urls = urls

    def download_page(self, url, page_num):
        """Retrieves the image data of a single page.
        
        Parameters
        ----------
        url : str
            The URL that links toward an image file.
        page_num : int
            The page number of the page.

        Returns
        -------
        ContentObject
            Object containing the page's image data, content type, page number, and the title
            of the music sheet.

        Raises
        ------
        RequestException
            If a problem arises during the request to retrieve content.
        """
        resp = requests.get(url)

        resp.raise_for_status()

        result = ContentObject(
            resp.content,
            resp.headers['Content-Type'],
            page_num,
            self.title,
        )

        return result

    def download_callback(self, future: Future[ContentObject]):
        """Callback function to be called when the download process of a single file is completed/
        
        Parameters
        ----------
        future : Future with return type of ContentObject
            The Future object that contains the result of the download process.

        Returns
        -------
        None        
        """
        logging.info(f"Successfully retrieved page {future.result().page_num}'s contents.")

    def execute(self): 
        """Executes the webscraping process as specified by the class.

        Returns
        -------
        list of ContentObject
            Ordered collection of data about the downloads' results.

        Raises
        ------
        TypeError
            If the URLs provided is not in a list or tuple.
        RequestException
            If a problem occurs in any of the request sent to retrieve the page content.
        """
        logging.info("Start downloading pages of the music sheet...")

        if not isinstance(self.urls, (list, tuple)):
            raise TypeError(f"Expected `urls` to be a list or tuple of str, not {type(self.urls)}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks: list[Future[ContentObject]] = []

            for i, url in enumerate(self.urls):
                logging.info(f"Retrieving contents of page {int(i) + 1}...")
                
                task = executor.submit(self.download_page, url, int(i) + 1)
                task.add_done_callback(self.download_callback)
                tasks.append(task)

        result: list[ContentObject] = []

        for task in tasks:
            if task.exception():
                raise task.exception()
            result.append(task.result())
                
        logging.info("Successfully retrieved all pages' contents.")
        
        return result

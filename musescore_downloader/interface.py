import os
import time
import logging
import argparse

from reportlab.lib.pagesizes import A4, LETTER

from . import log_handler
from .common.defaults import (
    SCROLLER_ELEMENT_ID,
    PAGE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS,
)
from .config_handler import initialize_config_handler
from .managers.path_manager import PathManager
from .file_generation.pdf_generator import PDFGenerator
from .file_generation.page_saver import PageSaver
from .web_scraper.page_file_scraper import PageFileScraper
from .web_scraper.score_scraper import ScoreScraper
from .web_scraper.selectors_generators import SelectorGenerators


def download_score(url):
    start = time.time()
    logging.info("Starting...")
    
    scroll_element_selector = SelectorGenerators.generate_id_selector(SCROLLER_ELEMENT_ID)
    page_container_selector = SelectorGenerators.generate_class_selector(PAGE_CONTAINER_CLASS)
    total_pages_container_selector = SelectorGenerators.generate_class_selector(TOTAL_PAGES_CONTAINER_CLASS)
    title_container_selector = SelectorGenerators.generate_class_selector(TITLE_CONTAINER_CLASS)

    pathmanager = PathManager()

    # 1. Retrieve links to each of the pages in the targeted music sheet
    score_scraper = ScoreScraper(
        scroll_element_selector, 
        page_container_selector, 
        total_pages_container_selector, 
        title_container_selector
    )
    
    score_scraper.initialize(use_headless=True)
    score_scraper.set_url(url)

    scraper_result = score_scraper.execute()
    if scraper_result is None:
        logging.error("Process terminated due to an error.")
        return

    # 2. Retrieve the page content from the extracted links
    pf_scraper = PageFileScraper(
        scraper_result.urls,
        scraper_result.title
    )
    pf_scraper_result = pf_scraper.execute()
    
    if pf_scraper_result is None:
        logging.error("Process terminated due to an error.")
        return

    # 3. Save the page content into files
    page_saver = PageSaver(
        scraper_result.title,
        pf_scraper_result,
        pathmanager
    )
    page_saver_result = page_saver.execute()

    if page_saver_result is None:
        logging.error("Process terminated due to an error.")
        return

    # 4. Merge the page files into one PDF
    pdf_generator = PDFGenerator(
        scraper_result.title,
        page_saver_result,
        A4,
        pathmanager
    )
    pdf_generator_result = pdf_generator.execute()

    if pdf_generator_result is False:
        logging.error("Process terminated due to an error.")
        return
    
    logging.info(f"Process finished in {time.time() - start} seconds.")
    return


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="python musescore_downloader.py",
        description=
            "Utility for downloading music sheet from Musescore.com.",
        epilog="Hello World",
    )

    arg_parser.add_argument("url", action="store", help="The Musescore URL from where to download the music sheet from.")
    args = arg_parser.parse_args()

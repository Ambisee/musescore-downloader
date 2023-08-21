import time
import logging

from reportlab.lib.pagesizes import A4

from ..initializers import handle_args, initialize_path_manager

from ...managers.path_manager import PathManager
from ...web_scraper.selector_generators import SelectorGenerators
from ...common.types.score_scraper_result import ScoreScraperResult
from ...common.constants import pagesize_alias_to_value
from ...common.defaults import (
    SCROLLER_ELEMENT_ID,
    PAGE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS
)

from ..scrape_score import scrape_score
from ..scrape_pages import scrape_pages
from ..save_pages import save_pages
from ..generate_pdf import generate_pdf
from ..delete_pagefiles import delete_pagefiles

def cli_main():
    start = time.time()
    logger.info("Starting...")

    args = handle_args()
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    logger = logging

    scroll_element_selector = SelectorGenerators.generate_id_selector(SCROLLER_ELEMENT_ID)
    page_container_selector = SelectorGenerators.generate_class_selector(PAGE_CONTAINER_CLASS)
    total_pages_container_selector = SelectorGenerators.generate_class_selector(TOTAL_PAGES_CONTAINER_CLASS)
    title_container_selector = SelectorGenerators.generate_class_selector(TITLE_CONTAINER_CLASS)
    
    page_size = A4
    if pagesize_alias_to_value.get(args.page_size) is not None:
        page_size = pagesize_alias_to_value[args.page_size]

    path_manager = initialize_path_manager(args, logger)
    if issubclass(type(path_manager), Exception):
        logger.error("Process terminated due to an error.")
        return -1
    

    # 1. Retrieve links to each of the pages in the targeted music sheet
    score_scrape_result: Exception | ScoreScraperResult = scrape_score(
        args.url,
        scroll_element_selector,
        page_container_selector,
        total_pages_container_selector,
        title_container_selector,
        logger
    )

    if issubclass(type(score_scrape_result), Exception):
        logger.error("Process terminated due to an error.")
        return -1


    # 2. Retrieve the page content from the extracted links
    page_scrape_result = scrape_pages(score_scrape_result, logger)
    
    if issubclass(type(page_scrape_result), Exception):
        logger.error("Process terminated due to an error.")
        return -1

    # 3. Save the page content into files
    page_saver_result = save_pages(
        score_scrape_result, 
        page_scrape_result, 
        path_manager, 
        logger
    )

    if issubclass(type(page_saver_result), Exception) :
        logger.error("Process terminated due to an error.")
        return -1

    # 4. Merge the page files into one PDF
    pdf_generation_result = generate_pdf(
        score_scrape_result,
        page_saver_result,
        page_size,
        path_manager,
        logger
    )
    
    if issubclass(type(pdf_generation_result), Exception):
        logger.error("Process terminated due to an error.")
        return -1
    
    if not args.save_pagefiles:
        delete_pagefiles(page_saver_result)

    logging.info(f"Process finished in {time.time() - start} seconds.")
    return 0

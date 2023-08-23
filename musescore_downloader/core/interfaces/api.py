import time
import logging

from reportlab.lib.pagesizes import A4

from ..initializers import handle_args, initialize_path_manager

from ...managers.path_manager import PathManager
from ...managers.selectors_manager import SelectorsManager
from ...common.types.score_scraper_result import ScoreScraperResult
from ...common.constants import pagesize_alias_to_value
from ...common.defaults import (
    SCROLLER_ELEMENT_ID,
    PAGE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS
)

from .. import (
    scrape_score,
    scrape_pages,
    save_pages,
    generate_pdf,
    delete_pagefiles
)

def api_main(
    url,
    filename,
    dirpath,
    page_size,
    save_pagefiles,
):
    start = time.time()
    logger = logging
    logger.info("Starting...")

    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

    scroll_element_selector = SelectorsManager.generate_id_selector(SCROLLER_ELEMENT_ID)
    page_container_selector = SelectorsManager.generate_class_selector(PAGE_CONTAINER_CLASS)
    total_pages_container_selector = SelectorsManager.generate_class_selector(TOTAL_PAGES_CONTAINER_CLASS)
    title_container_selector = SelectorsManager.generate_class_selector(TITLE_CONTAINER_CLASS)
    
    page_size = A4
    if pagesize_alias_to_value.get(page_size) is not None:
        page_size = pagesize_alias_to_value[page_size]

    path_manager: PathManager = initialize_path_manager(None, logger)
    if issubclass(type(path_manager), Exception):
        logger.error("Process terminated due to an error.")
        return -1
    

    # 1. Retrieve links to each of the pages in the targeted music sheet
    score_scrape_result: Exception | ScoreScraperResult = scrape_score(
        url,
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
    
    if not save_pagefiles:
        delete_pagefiles(page_saver_result)

    logging.info(f"Process finished in {time.time() - start} seconds.")
    return 0

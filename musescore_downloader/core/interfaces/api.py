import time
import logging
from typing import Literal

from reportlab.lib.pagesizes import A4


from ..initializers import handle_args, initialize_path_manager, initialize_selectors_manager
from ..validation.log_errors import log_validation_errors
from ..validate_input import validate_input
from ..download_score import download_score
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
    dirpath=None,
    page_size='A4',
    save_pagefiles=False
) -> Exception | dict[str, list[Exception]] | Literal[0]:
    start = time.time()
    logger = logging
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    
    logger.info("Starting...")

    validation_result = validate_input({
        'url': url, 
        'dirpath': dirpath, 
        'page_size': page_size, 
        'save_pagefiles': save_pagefiles
    })
    
    if len(validation_result.keys()) > 0:
        log_validation_errors(validation_result, logger)
        logger.error("Process terminated due to an error.")
        return validation_result

    page_size = A4
    if pagesize_alias_to_value.get(page_size) is not None:
        page_size = pagesize_alias_to_value[page_size]

    selectors_manager = initialize_selectors_manager()
    path_manager = initialize_path_manager({'dirpath': dirpath})
    if issubclass(type(path_manager), Exception):
        logger.error("Process terminated due to an error.")
        return path_manager

    result = download_score(
        url,
        selectors_manager,
        path_manager,
        page_size,
        save_pagefiles,
        logger
    )

    if issubclass(type(result), Exception):
        logger.error("Process terminated due to an error")
        return result

    logging.info(f"Process finished in {time.time() - start} seconds.")
    return 0

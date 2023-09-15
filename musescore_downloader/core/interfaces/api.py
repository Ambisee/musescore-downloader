import time
import logging
from typing import Literal

from reportlab.lib.pagesizes import A4

from ..validation.utils import log_validation_errors

from .. import (
    validate_input,
    download_score
)
from ..initializers import (
    initialize_args, 
    initialize_path_manager, 
    initialize_selectors_manager
)
from ..validation import (
    ValidationResult,
    log_validation_errors
)
from ...common.constants import pagesize_alias_to_value

from ..utils import (
    scrape_score,
    scrape_pages,
    save_pages,
    generate_pdf,
    delete_pagefiles
)

def api_main(
    url: str,
    dirpath: str | None = None,
    page_size: str ='A4',
    save_pagefiles: bool =False
) -> Exception | dict[str, ValidationResult] | Literal[0]:
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

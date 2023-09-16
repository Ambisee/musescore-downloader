import time
import logging

from reportlab.lib.pagesizes import A4

from ..initializers import (
    initialize_args, initialize_path_manager, initialize_selectors_manager
)

from ...managers.path_manager import PathManager
from ...common.constants import pagesize_alias_to_value
from ..validation import log_validation_errors

from ..utils import validate_input
from ..download_score import download_score

def cli_main() -> int:
    """Main entry point for the CLI.

    Returns
    -------
    int
        1 if the process exits successfully, 0 otherwise.    
    """
    start = time.time()

    logger = logging
    args = initialize_args()
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    logger.info("Starting...")

    logger.info("Validating inputs...")
    validation_result = validate_input(args.__dict__)
    
    if len(validation_result.keys()) > 0:
        log_validation_errors(validation_result, logger)
        logger.error("Process terminated due to an error.")
        return -1

    logger.info("Input validation finished.")

    page_size = A4
    if pagesize_alias_to_value.get(args.page_size) is not None:
        page_size = pagesize_alias_to_value[args.page_size]

    selectors_manager = initialize_selectors_manager()
    path_manager: PathManager = initialize_path_manager(args.__dict__)
    if issubclass(type(path_manager), Exception):
        logger.error(path_manager)
        logger.error("Process terminated due to an error.")
        return -1

    result: int | Exception = download_score(
        args.url,
        selectors_manager,
        path_manager,
        page_size,
        args.save_pagefiles,
        logger
    )

    if issubclass(type(result), Exception):
        return -1

    logging.info(f"Process finished in {time.time() - start} seconds.")
    return 0

from logging import Logger

from ..file_generation import PageSaver
from ..managers import PathManager
from ..common.types import (
    SaveCompleteObject, 
    ScoreScraperResult,
    ContentObject
)

def save_pages(
    scraper_result: ScoreScraperResult,
    pf_scraper_result: list[ContentObject],
    path_manager: PathManager,
    logger: Logger
) -> list[SaveCompleteObject] | Exception:
    page_saver = PageSaver(
        scraper_result.title,
        pf_scraper_result,
        path_manager
    )

    try:
        result = page_saver.execute()
    except Exception as e:
        logger.error(e)
        return e
    
    return result

from logging import Logger

from ...file_generation import PageSaver
from ...managers import PathManager
from ...common.exceptions.core import InvalidContentTypeError
from ...common.types import (
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
    """Saves the content of each individual files into their own file on the filesystem.

    Parameters
    ----------
    scraper_result : ScoreScraperResult
        The object that contains the title of the score.
    pf_scraper_result : list of ContentObject
        The collection of objects that contains page number and the content of individual page.
    path_manager : PathManager
        The object that contains the paths to the filesystem to store the contents to.
    logger : Logger
        The object that handles printing messages.
    
    Returns
    -------
    list of SaveCompleteObject or Exception
        If successful, the collection of objects that contains the path where each file is located.
        Else, an exception detailing the error encountered.
    """
    page_saver = PageSaver(
        scraper_result.title,
        pf_scraper_result,
        path_manager
    )

    try:
        result = page_saver.execute()
    except KeyError as e:
        logger.error(e)
        return InvalidContentTypeError(str(e))
    except Exception as e:
        logger.error(e)
        return e
    
    return result

import os
import os
from logging import Logger

from urllib.error import URLError
from selenium.common.exceptions import (
    NoSuchElementException,
    InvalidArgumentException,
)

from ...web_scraper import ScoreScraper
from ...managers import SelectorsManager
from ...common.types import ScoreScraperResult
from ...common.exceptions import (
    InvalidURLError, 
    UnexpectedError,
    NoConnectionError,
    PageElementNotFoundError,
    InitialElementNotFoundError,
)

def scrape_score(
    url: str,
    selectors_manager: SelectorsManager,
    logger: Logger
) -> ScoreScraperResult | Exception:
    """Scrapes the Musescore webpage for the URLs of the score's pages.

    Parameters
    ----------
    url : str
        The Musescore webpage URL.
    selectors_manager : SelectorsManager
        The object that stores the CSS selectors.
    logger : Logger
        The object that handles printing messages.

    Returns
    -------
    ScoreScraperResult or Exception
        If successful, the object that stores the result of the scraper. Else,
        An exception detailing the error encountered during the process.    
    """
    scraper = ScoreScraper(
        selectors_manager
    )

    scraper.set_url(url)
    debug = os.environ.get("DEBUG_ON", None)

    try:
        scraper.initialize(use_headless=False if debug is not None else True)
        result = scraper.execute()
    except URLError as e:
        message = (
            "The scraper cannot retrieve the webpage."
            " Please check your internet connection."
        )
        logger.error(message)
        return NoConnectionError(message)
    except InvalidArgumentException:
        message = (
            "The scraper cannot retrieve the webpage."
            " Please ensure that the web URL is a valid URL."
        )
        logger.error(message)
        return InvalidURLError(message)
    except InitialElementNotFoundError:
        message = (
            "The scraper cannot find the initial page of the music sheet."
            " Please ensure that the web URL is a valid Musescore URL."
            " If the URL is a valid Musescore URL, please report the issue"
            " at https://github.com/Ambisee/musescore-downloader/issues."
        )
        logger.error(message)
        return InvalidURLError(message)
    except PageElementNotFoundError as e:
        message = (
            f"The scraper cannot find the next page element of the music sheet (page {str(e)})."
            " An unexpected error has occured. Please report the issue at "
            "https://github.com/Ambisee/musescore-downloader/issues."
        )
        logger.error(message)
        return UnexpectedError(message)
    
    return result

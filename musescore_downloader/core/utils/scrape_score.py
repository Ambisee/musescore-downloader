import os
from logging import Logger

from urllib.error import URLError
from selenium.common.exceptions import (
    NoSuchElementException,
    InvalidArgumentException,
)

from ...web_scraper import ScoreScraper
from ...web_scraper.driver_factories import ChromeDriverFactory
from ...managers import SelectorsManager
from ...common.types import ScoreScraperResult
from ...common.exceptions import (
    InvalidURLError, 
    UnexpectedError,
    NoConnectionError,
    PageElementNotFoundError,
    InitialElementNotFoundError,
    MetadataElementNotFoundError,
)

def scrape_score(
    url: str,
    selectors_manager: SelectorsManager,
    logger: Logger,
    scraper_timeout: float = 10,
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
    scraper_timeout : float, default=10
        The maximum time for the scraper to wait for a specific state until timeout.

    Returns
    -------
    ScoreScraperResult or Exception
        If successful, the object that stores the result of the scraper. Else,
        An exception detailing the error encountered during the process.    
    """

    logger.info("Start...")
    executable_path = os.getenv("CHROME_DRIVER_PATH")
    driver = ChromeDriverFactory().create_driver(path=executable_path)

    scraper = ScoreScraper(
        selectors_manager,
        driver,
        timeout=scraper_timeout
    )

    scraper.set_url(url)
    
    try:
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
    except MetadataElementNotFoundError as e:
        message = (
            "The scraper cannot find the element that contains the {}."
            " Please report the issue at "
            "https://github.com/Ambisee/musescore-downloader/issues."
        )
        logger.error(message)
        return UnexpectedError(message)
    except PageElementNotFoundError as e:
        message = (
            f"The scraper cannot find the next page element of the music sheet (page {str(e)})."
            " An unexpected error has occured. Please report the issue at "
            "https://github.com/Ambisee/musescore-downloader/issues."
        )
        logger.error(message)
        return UnexpectedError(message)
    finally:
        scraper.shutdown_driver()
    
    return result

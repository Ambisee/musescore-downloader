from logging import Logger

from selenium.common.exceptions import NoSuchElementException

from ..web_scraper import (
    ScoreScraper,
)
from ..managers import SelectorsManager
from ..common.types import (
    ScoreScraperResult
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
    scraper.initialize()
    
    try:
        result = scraper.execute()
    except Exception as e:
        logger.error(e)
        return e
    
    return result

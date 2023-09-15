from logging import Logger

from ..web_scraper import PageFileScraper
from ..common.types import ScoreScraperResult, ContentObject

def scrape_pages(
    scraper_result: ScoreScraperResult,
    logger: Logger
) -> list[ContentObject] | Exception:
    """Fetches the file content of each page of the score's pages
    through the URLs of each page.

    Parameters
    ----------
    scraper_result : ScoreScraperResult
        The object that stores the title of the score and the URLs to each page.
    logger : Logger
        The object that handles printing out messages.

    Returns
    -------
    list[ContentObject] or Exception
        If successful, the list of objects containing the file content of each sheet page.
        Else, an exception detailing the error encountered during the process.
    """
    pf_scraper = PageFileScraper(
        scraper_result.urls,
        scraper_result.title
    )

    try:
        result = pf_scraper.execute()
    except Exception as e:
        logger.error(e)
        return e

    return result

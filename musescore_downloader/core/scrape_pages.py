from logging import Logger

from ..web_scraper import PageFileScraper
from ..common.types import ScoreScraperResult, ContentObject

def scrape_pages(
    scraper_result: ScoreScraperResult,
    logger: Logger
) -> list[ContentObject] | Exception:
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

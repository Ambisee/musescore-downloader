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

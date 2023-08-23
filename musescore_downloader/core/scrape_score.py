from selenium.common.exceptions import NoSuchElementException

from ..web_scraper.score_scraper import (
    ScoreScraper,
    UninitializedWebDriverError
)

def scrape_score(
    url,
    selectors_manager,
    logger
):
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

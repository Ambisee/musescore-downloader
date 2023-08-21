from selenium.common.exceptions import NoSuchElementException

from ..web_scraper.score_scraper import (
    ScoreScraper,
    UninitializedWebDriverError
)

def scrape_score(
    url,
    scroll_element_selector,
    page_container_selector,
    total_pages_container_selector,
    title_container_selector,
    logger
):
    scraper = ScoreScraper(
        scroll_element_selector,
        page_container_selector,
        total_pages_container_selector,
        title_container_selector
    )

    scraper.set_url(url)
    scraper.initialize()
    
    try:
        result = scraper.execute()
    except Exception as e:
        logger.error(e)
        return e
    
    return result

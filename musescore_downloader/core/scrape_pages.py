from ..web_scraper.page_file_scraper import PageFileScraper

def scrape_pages(
    scraper_result,
    logger
):
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

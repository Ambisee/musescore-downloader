from ..file_generation.page_saver import PageSaver

def save_pages(
    scraper_result,
    pf_scraper_result,
    path_manager,
    logger
):
    page_saver = PageSaver(
        scraper_result.title,
        pf_scraper_result,
        path_manager
    )

    try:
        result = page_saver.execute()
    except Exception as e:
        logger.error(e)
        return e
    
    return  result

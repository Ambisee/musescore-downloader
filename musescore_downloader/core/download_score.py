from ..common.types.score_scraper_result import ScoreScraperResult
from ..common.types.save_complete_object import SaveCompleteObject
from ..common.types.content_object import ContentObject

from .scrape_score import scrape_score
from .scrape_pages import scrape_pages
from .save_pages import save_pages
from .generate_pdf import generate_pdf
from .delete_pagefiles import delete_pagefiles

def download_score(
    url,
    selectors_manager,
    path_manager,
    page_size,
    save_pagefiles,
    logger,
):
    # 1. Retrieve links to each of the pages in the targeted music sheet
    score_scrape_result: Exception | ScoreScraperResult = scrape_score(
        url,
        selectors_manager,
        logger
    )

    if issubclass(type(score_scrape_result), Exception):
        logger.error("Process terminated due to an error.")
        return score_scrape_result


    # 2. Retrieve the page content from the extracted links
    page_scrape_result: Exception | ContentObject = scrape_pages(score_scrape_result, logger)
    
    if issubclass(type(page_scrape_result), Exception):
        logger.error("Process terminated due to an error.")
        return page_scrape_result

    # 3. Save the page content into files
    page_saver_result: Exception | list[SaveCompleteObject] = save_pages(
        score_scrape_result, 
        page_scrape_result, 
        path_manager, 
        logger
    )

    if issubclass(type(page_saver_result), Exception) :
        logger.error("Process terminated due to an error.")
        return page_saver_result

    # 4. Merge the page files into one PDF
    pdf_generation_result = generate_pdf(
        score_scrape_result,
        page_saver_result,
        page_size,
        path_manager,
        logger
    )
    
    if issubclass(type(pdf_generation_result), Exception):
        logger.error("Process terminated due to an error.")
        return pdf_generation_result
    
    if not save_pagefiles:
        delete_pagefiles(page_saver_result)

    return 0
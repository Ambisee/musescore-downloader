from logging import Logger

from ..managers import SelectorsManager, PathManager
from ..common.types import (
    ScoreScraperResult, 
    SaveCompleteObject, 
    ContentObject
)

from .utils import (
    scrape_score, 
    scrape_pages, 
    save_pages, 
    generate_pdf, 
    delete_pagefiles
)

def download_score(
    url: str,
    selectors_manager: SelectorsManager,
    path_manager: PathManager,
    page_size: tuple[float, float],
    save_pagefiles: bool,
    logger: Logger,
) -> str | Exception:
    """Downloads a Musescore music sheet as a PDF.
    
    Parameters
    ----------
    url : str
        The Musescore URL that contains the music sheet.
    selectors_manager : SelectorsManager
        The object that contains the relevant CSS selectors.
    path_manager : PathManager
        The object that stores the paths on the filesystem to store the files into.
    page_size : tuple of two floats
        The dimensions of the pages in the resulting PDF. Must contain exactly two float values denoting the
        width and height respectively.
    save_pagefiles : bool
        Whether or not to save the individual page files.
    logger : Logger
        The object that handles printing messages.

    Returns
    -------
    str or Exception
        If successful, returns the filepath to the PDF.
        Else, an exception detailing the error encountered.
    """
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
    pdf_generation_result: Exception | str = generate_pdf(
        score_scrape_result,
        page_saver_result,
        page_size,
        path_manager,
        logger
    )
    
    if issubclass(type(pdf_generation_result), Exception):
        logger.error("Process terminated due to an error.")
    
    if not save_pagefiles:
        delete_pagefiles(page_saver_result)

    return pdf_generation_result

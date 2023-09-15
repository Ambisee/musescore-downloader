from logging import Logger

from ...managers import PathManager
from ...file_generation import PDFGenerator
from ...common.types import ScoreScraperResult, SaveCompleteObject

def generate_pdf(
    scraper_result: ScoreScraperResult,
    page_saver_result: list[SaveCompleteObject],
    page_size: tuple[float, float],
    path_manager: PathManager,
    logger: Logger
) -> None | Exception:
    """Merges the page files into a single PDF file and saves it into the filesystem.

    Parameters
    ----------
    scraper_result : ScoreScraperResult
        The object that contains the title of the score.
    page_saver_result : list of SaveCompleteObject
        The list of object that contains the path to a page file.
    page_size : tuple of two floats
        The dimensions of the pages in the resulting PDF. Must contain exactly two float values denoting the
        width and height respectively.
    path_manager : PathManager
        The object that contains the paths on the filesystem to store the files into.
    logger : Logger
        The object that handles printing messages.

    Returns
    -------
    None or Exception
        If successful, nothing is returned.
        Else, an exception detailing the error encountered.
    """
    pdf_generator = PDFGenerator(
        scraper_result.title,
        page_saver_result,
        page_size,
        path_manager
    )
    
    try:    
        result = pdf_generator.execute()
    except Exception as e:
        logger.error(e)
        return e
    
    return result

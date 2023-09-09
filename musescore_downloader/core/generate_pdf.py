from logging import Logger

from ..managers import PathManager
from ..file_generation import PDFGenerator
from ..common.types import ScoreScraperResult, SaveCompleteObject

def generate_pdf(
    scraper_result: ScoreScraperResult,
    page_saver_result: list[SaveCompleteObject],
    page_size: tuple[float, float],
    path_manager: PathManager,
    logger: Logger
) -> Exception | None:
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

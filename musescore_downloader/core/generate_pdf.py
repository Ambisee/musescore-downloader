from ..file_generation.pdf_generator import PDFGenerator

def generate_pdf(
    scraper_result,
    page_saver_result,
    page_size,
    path_manager,
    logger
):
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

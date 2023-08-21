import os
import logging

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.testdrawings import Drawing
from reportlab.lib.pagesizes import A4, LETTER

from PIL.Image import open

from ..managers.path_manager import PathManager
from ..common.types.save_complete_object import SaveCompleteObject

class UnrecognizedFiletypeError(Exception):
    """Encountered a file with a foreign filetype."""

class PDFGenerator:
    """Puts together the page files into a single PDF file.
    
    Attributes
    ----------
    title : str
        The title of the music sheet
    save_complete_objects : list of SaveCompleteObject
        A list of objects containing information about each page files.
    page_size : tuple of float
        The dimension of the pages of the PDF file. The tuple must have exactly 2 elements. First element represents
        the `width` of the page and the second element represents the `height` of the page.
    path_manager : PathManager
        Object that manages the output paths.
    """
    def __init__(
        self,
        title: str,
        save_complete_objects: list[SaveCompleteObject],
        page_size: tuple[float, float],
        path_manager: PathManager
    ):
        self.title = title
        self.save_complete_objects = save_complete_objects
        self.page_size = page_size
        self.path_manager = path_manager
    
    def set_page_size(self, page_size: tuple[float, float]):
        self.page_size = page_size

    def scale_to_fit_page(self, drawing: Drawing):
        """Resizes an SVG file into the dimensions of the page.
        
        Parameters
        ----------
        drawing : Drawing
            A reportlab Drawing object.
        
        Returns
        -------
        None
        """
        drawing.scale(self.page_size[0] / drawing.width, self.page_size[1] / drawing.height)

    def add_svg(self, canvas: Canvas, save_complete_object: SaveCompleteObject):
        """Adds a page file of type SVG into the PDF.

        Parameters
        ----------
        canvas : Canvas        
            Object that represents the PDF file.
        save_complete_object : SaveCompleteObject
            Object that stores information about the page file.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Incorrect filetype of file referenced by the path contained in the SaveCompleteObject.
        """
        path = save_complete_object.path
        extension = os.path.splitext(path)[1]

        if extension != ".svg":
            raise ValueError(f"Expected path to end with '.svg' but the file for page {save_complete_object.page_num} has the extension '{extension}'")

        page_drawing = svg2rlg(path)
        self.scale_to_fit_page(page_drawing)

        renderPDF.draw(page_drawing, canvas, 0, 0)

    def add_png(self, canvas: Canvas, save_complete_object: SaveCompleteObject):
        """Adds a page file of type PNG into the PDF.

        Parameters
        ----------
        canvas : Canvas        
            Object that represents the PDF file.
        save_complete_object : SaveCompleteObject
            Object that stores information about the page file.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Incorrect filetype of file referenced by the path contained in the SaveCompleteObject.
        """
        path = save_complete_object.path
        extension = os.path.splitext(path)[1]

        if extension != ".png":
            raise ValueError(f"Expected path to end with '.png' but the file for page {save_complete_object.page_num} has the extension '{extension}'")

        page_drawing = open(path)
        canvas.drawInlineImage(page_drawing, 0, 0, *self.page_size)
    
    def execute(self):
        """Executes the process.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Incorrect handling of file.
        UnrecognizedFiletypeError
            Found a page file with a foreign filetype.
        """
        logging.info("Merging saved contents into a PDF file...")

        output_path = self.path_manager.get_output_filepath(self.title)
        file = Canvas(
            output_path, 
            self.page_size
        )

        for save_complete_object in self.save_complete_objects:
            if save_complete_object.filetype == ".svg":
                self.add_svg(file, save_complete_object)
            elif save_complete_object.filetype == ".png":
                self.add_png(file, save_complete_object)
            else:
                raise UnrecognizedFiletypeError(f"Encountered a foreign filetype : {save_complete_object.filetype}")
            
            file.showPage()
        
        file.save()
        logging.info(f"Finished putting everything into a PDF file.")

        return

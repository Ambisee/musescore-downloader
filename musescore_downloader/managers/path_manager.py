import os

from pathvalidate import validate_filepath, validate_filename

class PathManager:
    """Manages the file and directory paths where the files will be saved.
    
    Attributes
    ----------
    page_image_dir_format : str, default="./output/%(title)s/pages"
        Directory format to store the page files. The format must include the `%(title)s` variable placeholder.
    page_image_filename_format : str, default="page_%(page_num)s%(extension)s"
        Filename format to name each page files. The format must include both the `%(page_num)s` and `%(extension)s` variable placeholder.
    output_dir_format : str, default="./output/%(title)s"
        Directory to store the resulting PDF file. The format must include the `%(title)s` variable placeholder.
    output_filename_format : str, default="%(title)s.pdf"
        Filename format of the resulting PDF file. The format must include the `%(title)s` variable placeholder and must end with the `.pdf` extension.
    """

    # Defaults
    page_image_dir_format = os.path.join(".", "output", "%(title)s", "pages")
    page_image_filename_format = "page_%(page_num)s%(extension)s"
    output_dir_format = os.path.join(".", "output", "%(title)s")
    output_filename_format = "%(title)s.pdf"

    test_dir_format_obj = {'title': 'foo'}
    test_filename_format_obj = {'title': 'foo', 'page_num': 0, 'extension': '.svg'}

    def __init__(
        self,
        page_image_dir_format=None,
        page_image_filename_format=None,
        output_dir_format=None,
        output_filename_format=None,
    ):
        self.set_page_image_dir_format(page_image_dir_format)
        self.set_page_image_filename_format(page_image_filename_format)
        self.set_output_dir_format(output_dir_format)
        self.set_output_filename_format(output_filename_format)

    def set_output_filename_format(self, output_filename_format):
        """Set the output filename's format

        Parameter
        ---------
        output_filename_format : str
            The format of the resulting PDF file. Must include the substring `%(title)s` and must end with the `.pdf` extension.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            The provided path is missing one or more placeholder variable(s).
        pathvalidate.error.ValidationError
        - ErrorReason.INVALID_CHARACTER : The filepath contains invalid characters.
        - ErrorReason.INVALID_LENGTH : The filepath exceeds the maximum length for a filepath.
        """

        if output_filename_format is None:
            self.output_filename_format = PathManager.output_filename_format
            return
        
        if "%(title)s" not in output_filename_format:
            raise ValueError("The provided directory format does not contain a %(title)s placeholder.")
        
        validate_filepath(output_filename_format % PathManager.test_dir_format_obj)
        self.output_filename_format = output_filename_format

    def set_output_dir_format(self, output_dir_format):
        """Sets the format of the directory path where the PDF file will be saved into.

        Parameters
        ----------
        output_dir_format : str
            The format of the directory. Must include the `%(title)s` substring.
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            The provided path is missing one or more placeholder variable(s).
        pathvalidate.error.ValidationError
        - ErrorReason.INVALID_CHARACTER : The filepath contains invalid characters.
        - ErrorReason.INVALID_LENGTH : The filepath exceeds the maximum length for a filepath.
        """
        if output_dir_format is None:
            self.output_dir_format = PathManager.output_dir_format
            return
        
        if "%(title)s" not in output_dir_format:
            raise ValueError("The provided directory format does not contain a %(title)s placeholder.")
        
        validate_filepath(output_dir_format % PathManager.test_dir_format_obj)
        self.output_dir_format = output_dir_format

    def set_page_image_dir_format(self, page_image_dir_format):
        """Sets the format of the directory path where the page files will be stored in. 

        Parameters
        ----------
        page_image_dir_format : str
            The format of the directory. Must include the `%(title)s` substring.
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            The provided path is missing one or more placeholder variable(s).
        pathvalidate.error.ValidationError
        - ErrorReason.INVALID_CHARACTER : The filepath contains invalid characters.
        - ErrorReason.INVALID_LENGTH : The filepath exceeds the maximum length for a filepath.
        """
        if page_image_dir_format is None:
            self.page_image_dir_format = PathManager.page_image_dir_format
            return
        
        if "%(title)s" not in page_image_dir_format:
            raise ValueError("The provided directory format does not contain a %(title)s placeholder.")
        
        validate_filepath(page_image_dir_format % PathManager.test_dir_format_obj)
        self.page_image_dir_format = page_image_dir_format

    def set_page_image_filename_format(self, page_image_filename_format):
        """Sets the format of the filename of the page files.

        Parameters
        ----------
        page_image_filename_format : str
            The format of the filename. Must include the `%(title)s` and the `%(page_num)s` substrings.
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            The provided path is missing one or more placeholder variable(s).
        pathvalidate.error.ValidationError
        - ErrorReason.INVALID_CHARACTER : The filepath contains invalid characters.
        - ErrorReason.INVALID_LENGTH : The filepath exceeds the maximum length for a filepath.
        """
        if page_image_filename_format is None:
            self.page_image_filename_format = PathManager.page_image_filename_format
            return
        
        if not all(placeholder in page_image_filename_format for placeholder in ["%(page_num)s", "%(extension)s"]):
            raise ValueError(
                "The provided filename format does not contain a %(page_num)s placeholder." \
                " Please provide a format that contains both %(page_num)s and %(extension)s placehoders."
            )
        
        validate_filename(page_image_filename_format % PathManager.test_filename_format_obj)
        self.page_image_filename_format = page_image_filename_format

    def get_page_image_filepath(self, page_num, title, extension):
        """Gets a formatted page file path.

        Parameters
        ----------
        page_num : int
            The page number associated with the file
        title : str
            The title of the music sheet associated with the file
        extension : str
            The file extension of the file. (e.g. .svg, .png, .jpg, etc.)
        
        Returns
        -------
        str
            A formatted file path.
        """
        return os.path.join(self.page_image_dir_format, self.page_image_filename_format) % {
            'title': title,
            'page_num': page_num,
            'extension': extension
        }

    def get_output_filepath(self, title):
        """Gets a formatted path to the resulting PDF file.
        
        Parameters
        ----------
        title : str
            The title of the music sheet.
        
        Returns
        -------
        str
            A formatted file path.
        """
        return os.path.join(self.output_dir_format, self.output_filename_format) % {
            'title': title
        }

    def get_page_image_dir(self, title):
        """Gets a formatted path to the directory containing the page files.

        Parameters
        ----------
        title : str
            The title of the music sheet.
        
        Returns
        -------
        str
            The formatted directory path.
        """
        return self.page_image_dir_format % {
            'title': title
        }
    
    def get_output_dir(self, title):
        """Gets a formatted path to a directory where the resulting PDF file will be placed in.

        Parameters
        ----------
        title : str
            The title of the music sheet.
        
        Returns
        -------
        str
            The formatted directory path.
        """
        return self.output_dir_format % {
            'title': title
        }

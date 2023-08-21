from argparse import (
    ArgumentParser,
    Namespace
)

from ..managers.path_manager import PathManager

def handle_args():
    parser = ArgumentParser(
        prog="musescore_downloader",
        description="Utility for downloading music sheet from Musescore.com.",
        add_help=True
    )

    parser.add_argument(
        "url",
        help="Musescore URL from where to download the music sheet from."
    )
    parser.add_argument(
        "--filename", 
        help="sets the filename format of the resulting PDF file. Must include the %%(title)s variable placeholder."
    )
    parser.add_argument(
        "--dirpath", 
        help="sets the filename format of the resulting PDF file. Must include the %%(title)s variable placeholder."
    )
    parser.add_argument(
        "--save-pagefiles",
        help="sets whether to keep the pagefiles after the program ends.",
        type=bool
    )
    parser.add_argument(
        "--page_size",
        help="the page size of the output PDF. Allowed values include the following literals: 'A4', 'LETTER'."
    )

    args = parser.parse_args()
    return args

def initialize_path_manager(arguments: Namespace, logger):
    path_manager = PathManager()

    try:
        if arguments.filename is not None:
            path_manager.set_output_filename_format(arguments.filename)
        if arguments.dirpath is not None:
            path_manager.set_output_filename_format(arguments.dirpath)
    except Exception as e:
        logger.error(e)
        return e

    return path_manager

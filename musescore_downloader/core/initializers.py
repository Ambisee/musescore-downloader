import os
from argparse import (
    ArgumentParser,
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
        "--dirpath", 
        help="sets the directory path to store the output files. Must include the %%(title)s variable placeholder.",
        type=str
    )
    parser.add_argument(
        "--page-size",
        help="the page size of the output PDF. Allowed values include the following literals: 'A4', 'LETTER'.",
    )
    parser.add_argument(
        "--save-pagefiles",
        help="sets whether to keep the pagefiles after the program ends.",
        action="store_true"
    )

    args = parser.parse_args()
    return args

def initialize_path_manager(path_manager_args):
    path_manager = PathManager()
 
    try:
        if path_manager_args.dirpath is not None:
            path_manager.set_output_dir_format(path_manager_args.dirpath)
            path_manager.set_page_image_dir_format(os.path.join(path_manager_args.dirpath, "pages"))
    except Exception as e:
        return e

    return path_manager

import os
from argparse import (
    ArgumentParser,
    Namespace
)

from ..managers.path_manager import PathManager
from ..managers.selectors_manager import SelectorsManager
from ..common.defaults import (
    SCROLLER_ELEMENT_ID,
    PAGE_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS   
)

def handle_args() -> Namespace:
    parser = ArgumentParser(
        prog="musescore-downloader",
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
        default='A4',
        type=str
    )
    parser.add_argument(
        "--save-pagefiles",
        help="sets whether to keep the pagefiles after the program ends.",
        action="store_true",
    )

    args = parser.parse_args()
    return args

def initialize_path_manager(path_manager_args: dict) -> PathManager | Exception:
    path_manager = PathManager()

    try:
        if path_manager_args.get("dirpath", None) is not None:
            path_manager.set_output_dir_format(path_manager_args['dirpath'])
            path_manager.set_page_image_dir_format(os.path.join(path_manager_args['dirpath'], "pages"))
    except Exception as e:
        return e

    return path_manager

def initialize_selectors_manager() -> SelectorsManager:
    selectors_manager = SelectorsManager(
        scroll_element_id=SCROLLER_ELEMENT_ID,
        page_container_class=PAGE_CONTAINER_CLASS,
        total_pages_container_class=TOTAL_PAGES_CONTAINER_CLASS,
        title_container_class=TITLE_CONTAINER_CLASS
    )

    return selectors_manager
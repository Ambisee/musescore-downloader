import os
import logging

import pytest
from reportlab.lib.pagesizes import A4
from selenium.common.exceptions import NoSuchElementException

from musescore_downloader import download_score
from musescore_downloader.managers.path_manager import PathManager
from musescore_downloader.managers.selectors_manager import SelectorsManager
from musescore_downloader.common.defaults import (
    PAGE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS,
    SCROLLER_ELEMENT_ID
)


selectors_manager = SelectorsManager(
        SCROLLER_ELEMENT_ID,
        PAGE_CONTAINER_CLASS,
        TOTAL_PAGES_CONTAINER_CLASS,
        TITLE_CONTAINER_CLASS
    )

path_manager = PathManager()

def test_simple():
    result = download_score(
        "https://musescore.com/user/48323/scores/4982298",
        selectors_manager,
        path_manager,
        A4,
        False,
        logging
    )

    assert result == 0
    assert os.path.exists(
        "./output/River Flows in You - Yiruma - 10th Anniversary Version (Piano)/River Flows in You - Yiruma - 10th Anniversary Version (Piano).pdf"
    ) == True

def test_main_incorrect_url():
    result = download_score(
        "https://google.com",
        selectors_manager,
        path_manager,
        A4,
        False,
        logging
    )

    assert type(result) == NoSuchElementException

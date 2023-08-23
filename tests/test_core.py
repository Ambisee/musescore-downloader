import os
import shutil
import logging

import pytest
from reportlab.lib.pagesizes import A4
from selenium.common.exceptions import NoSuchElementException

from musescore_downloader import api_main
from musescore_downloader.common.defaults import (
    PAGE_CONTAINER_CLASS,
    TOTAL_PAGES_CONTAINER_CLASS,
    TITLE_CONTAINER_CLASS,
    SCROLLER_ELEMENT_ID
)

@pytest.fixture
def MUSESCORE_URL():
    return "https://musescore.com/user/48323/scores/4982298"

@pytest.fixture
def OUTPUT_DIR():
    return "./output"

@pytest.fixture(autouse=True)
def clean_dir():
    yield
    
    if os.path.exists("./output"):
        shutil.rmtree("./output")

def test_simple(MUSESCORE_URL):
    result = api_main(
        MUSESCORE_URL
    )

    assert result == 0
    assert os.path.exists(
        "./"
        "output/"
        "River Flows in You - Yiruma - 10th Anniversary Version (Piano)/"
        "River Flows in You - Yiruma - 10th Anniversary Version (Piano).pdf"
    ) == True

def test_main_incorrect_url():
    result = api_main(
        "https://google.com"
    )

    assert isinstance(result, NoSuchElementException)

def test_main_incorrect_pagesize(MUSESCORE_URL):
    result = api_main(
        MUSESCORE_URL,
        page_size='F4'
    )

    assert type(result) == dict
    assert result.get('page_size') is not None
    assert len(result['page_size']) > 0
    assert isinstance(result['page_size'][0], ValueError)
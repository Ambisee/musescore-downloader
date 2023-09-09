import os
import shutil

import pytest
from reportlab.lib.pagesizes import A4
from selenium.common.exceptions import NoSuchElementException

from musescore_downloader import api_main
from musescore_downloader.core.validation import ValidationResult

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
        page_size='some_non_existent_pagesize'
    )

    assert type(result) == dict
    assert result.get('page_size') is not None

    assert isinstance(result.get('page_size'), ValidationResult)
    
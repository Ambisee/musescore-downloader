import os

from reportlab.lib.pagesizes import A4

from musescore_downloader import api_main
from musescore_downloader.common.exceptions.core import InvalidURLError
from musescore_downloader.core.validation import ValidationResult


def test_simple(MUSESCORE_URL: str):
    result = api_main(
        MUSESCORE_URL
    )

    assert isinstance(result, str)
    assert os.path.exists(
        "./"
        "output/"
        "River Flows in You - Yiruma - 10th Anniversary Version (Piano)/"
        "River Flows in You - Yiruma - 10th Anniversary Version (Piano).pdf"
    ) == True

def test_incorrect_valid_url(INVALID_DOMAIN_URL: str):
    result = api_main(
        INVALID_DOMAIN_URL
    )

    assert isinstance(result, InvalidURLError)

def test_incorrect_invalid_url(INVALID_SCHEMA_URL: str):
    result = api_main(
        INVALID_SCHEMA_URL
    )

    assert isinstance(result, InvalidURLError)

def test_incorrect_pagesize_value(MUSESCORE_URL: str):
    result = api_main(
        MUSESCORE_URL,
        page_size='some_non_existent_pagesize'
    )

    assert type(result) == dict
    assert result.get('page_size') is not None

    assert isinstance(result.get('page_size'), ValidationResult)

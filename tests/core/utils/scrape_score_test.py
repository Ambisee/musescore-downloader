from logging import Logger

from musescore_downloader.core.utils import scrape_score
from musescore_downloader.common.types import ScoreScraperResult
from musescore_downloader.common.exceptions.core import (
    InvalidURLError
)
from musescore_downloader.managers import (
    SelectorsManager, 
    PathManager
)

def test_score_scrape_simple(
    MUSESCORE_URL: str,
    SELECTORS_MANAGER: SelectorsManager,
    LOGGER: Logger
):
    result = scrape_score(
        MUSESCORE_URL,
        SELECTORS_MANAGER,
        LOGGER
    )

    assert isinstance(result, ScoreScraperResult)
    assert isinstance(result.num_of_pages, int)
    assert isinstance(result.title, str)
    assert isinstance(result.urls, (list, tuple))
    assert len(result.urls) == 4
    assert isinstance(result.urls[0], str)

def test_score_scraper_invalid_domain_url(
    INVALID_DOMAIN_URL: str,
    SELECTORS_MANAGER: SelectorsManager,
    LOGGER: Logger
):
    result = scrape_score(
        INVALID_DOMAIN_URL,
        SELECTORS_MANAGER,
        LOGGER
    )

    assert isinstance(result, InvalidURLError)

def test_score_scraper_invalid_schema_url(
    INVALID_SCHEMA_URL: str,
    SELECTORS_MANAGER: SelectorsManager,
    LOGGER: Logger
):
    result = scrape_score(
        INVALID_SCHEMA_URL,
        SELECTORS_MANAGER,
        LOGGER
    )

    assert isinstance(result, InvalidURLError)

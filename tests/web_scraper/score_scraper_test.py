import pytest

from musescore_downloader.web_scraper import ScoreScraper
from musescore_downloader.common.types import ScoreScraperResult
from musescore_downloader.core import initialize_selectors_manager

@pytest.fixture
def SCORE_SCRAPER(SELECTORS_MANAGER):
    return ScoreScraper(
        SELECTORS_MANAGER
    )


def test_simple(SCORE_SCRAPER, MUSESCORE_URL):
    SCORE_SCRAPER.set_url(MUSESCORE_URL)
    res = SCORE_SCRAPER.execute()

    assert isinstance(res, ScoreScraperResult)
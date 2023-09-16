import pytest

from musescore_downloader.web_scraper import ScoreScraper
from musescore_downloader.common.types import ScoreScraperResult
from musescore_downloader.core import initialize_selectors_manager

@pytest.fixture
def SCORE_SCRAPER(SELECTORS_MANAGER):
    return ScoreScraper(
        SELECTORS_MANAGER
    )


def test_simple(SCORE_SCRAPER: ScoreScraper, MUSESCORE_URL):
    SCORE_SCRAPER.set_url(MUSESCORE_URL)
    SCORE_SCRAPER.initialize()

    res = SCORE_SCRAPER.execute()

    assert isinstance(res, ScoreScraperResult)


def test_incorrect_init_args(SCORE_SCRAPER: ScoreScraper):
    with pytest.raises(TypeError):
        SCORE_SCRAPER.initialize(window_size=10)

    with pytest.raises(ValueError):
        SCORE_SCRAPER.initialize(window_size=(1,2,3,4))

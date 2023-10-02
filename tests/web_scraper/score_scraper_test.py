import pytest

from musescore_downloader.web_scraper import ScoreScraper
from musescore_downloader.web_scraper.driver_factories import ChromeDriverFactory
from musescore_downloader.common.types import ScoreScraperResult
from musescore_downloader.core import initialize_selectors_manager

@pytest.fixture
def SCORE_SCRAPER(SELECTORS_MANAGER):
    driver = ChromeDriverFactory().create_driver()

    return ScoreScraper(
        SELECTORS_MANAGER,
        driver
    )

def test_simple(SCORE_SCRAPER: ScoreScraper, MUSESCORE_URL):
    SCORE_SCRAPER.set_url(MUSESCORE_URL)

    res = SCORE_SCRAPER.execute()

    assert isinstance(res, ScoreScraperResult)

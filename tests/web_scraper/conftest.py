import pytest

from musescore_downloader.core import (
    initialize_path_manager,
    initialize_selectors_manager
)

@pytest.fixture
def PATH_MANAGER():
    return initialize_path_manager({})


@pytest.fixture
def SELECTORS_MANAGER():
    return initialize_selectors_manager()

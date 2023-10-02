import os
import shutil
import logging

import pytest

from musescore_downloader.core.initializers import (
    initialize_selectors_manager,
    initialize_path_manager
)

@pytest.fixture(scope="session")
def MUSESCORE_URL():
    return "https://musescore.com/user/48323/scores/4982298"


@pytest.fixture(scope="session")
def OUTPUT_DIR():
    return "./output"

@pytest.fixture
def SELECTORS_MANAGER():
    return initialize_selectors_manager()

@pytest.fixture
def PATH_MANAGER():
    return initialize_path_manager({})

@pytest.fixture
def INVALID_DOMAIN_URL():
    return "https://www.google.com"

@pytest.fixture
def INVALID_SCHEMA_URL():
    return "this_is-an=invalid$%schema"

@pytest.fixture
def LOGGER():
    return logging

@pytest.fixture(autouse=True)
def clean_dir():
    yield
    
    if os.path.exists("./output"):
        shutil.rmtree("./output")
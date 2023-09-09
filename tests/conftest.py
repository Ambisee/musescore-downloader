import os
import shutil
import pytest

@pytest.fixture(scope="session")
def MUSESCORE_URL():
    return "https://musescore.com/user/48323/scores/4982298"

@pytest.fixture(scope="session")
def OUTPUT_DIR():
    return "./output"

@pytest.fixture(autouse=True)
def clean_dir():
    yield
    
    if os.path.exists("./output"):
        shutil.rmtree("./output")
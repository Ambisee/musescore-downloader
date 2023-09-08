from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'A web scraper for scraping music sheets from musescore.'

# Setting up
setup(
    name="musescore_downloader",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'selenium', 'web scraper', 'musescore'],
    entry_points={
        'console scripts': [
            'musescore_downloader = musescore_downloader:cli_main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
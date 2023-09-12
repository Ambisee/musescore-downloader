import pytest

from musescore_downloader.core.validation import (
    ValidationPipeline,
    ValidationResult,
    ValueValidator,
    TypeValidator
)


@pytest.fixture
def pipeline():
    return ValidationPipeline()


def test_simple(pipeline: ValidationPipeline):
    pipeline.add_validator("arg0", ValueValidator(-1))

    res_valid = pipeline.validate({"arg0": -1})
    
    assert isinstance(res_valid, dict)
    assert len(res_valid) == 0

    res_invalid = pipeline.validate({"arg0": 0})

    assert isinstance(res_invalid, dict)
    assert len(res_invalid) == 1
    assert isinstance(res_invalid.get("arg0"), ValidationResult)
    assert not res_invalid.get("arg0").is_valid()

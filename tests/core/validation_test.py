import pytest

from musescore_downloader.core.validation import (
    ValidationPipeline,
    ValidationResult,
    ValueValidator,
    TypeValidator,
    ANDValidator,
    ORValidator,
    ExternalValidator,
    ValidationFunction
)


@pytest.fixture
def pipeline():
    return ValidationPipeline()

def test_value_validator(pipeline: ValidationPipeline):
    pipeline.add_validator("arg0", ValueValidator(-1))

    res_valid = pipeline.validate({"arg0": -1})
    
    assert isinstance(res_valid, dict)
    assert len(res_valid) == 0

    res_invalid = pipeline.validate({"arg0": 0})

    assert isinstance(res_invalid, dict)
    assert len(res_invalid) == 1
    assert isinstance(res_invalid.get("arg0"), ValidationResult)

def test_type_validator(pipeline: ValidationPipeline):
    pipeline.add_validator("arg0", TypeValidator(str))

    res_valid = pipeline.validate({"arg0": "hello"})

    assert isinstance(res_valid, dict)
    assert len(res_valid) == 0

    res_invalid = pipeline.validate({"arg0": 10})

    assert isinstance(res_invalid, dict)
    assert len(res_invalid) == 1
    assert isinstance(res_invalid.get("arg0"), ValidationResult)

def test_external_validator(pipeline: ValidationPipeline):
    pipeline.add_validator("arg0", ExternalValidator(ValidationFunction(lambda val: len(val) <= 2)))

    res_valid = pipeline.validate({"arg0": "ap"})

    assert isinstance(res_valid, dict)
    assert len(res_valid) == 0

    res_invalid = pipeline.validate({"arg0": "applied"})

    assert isinstance(res_invalid, dict)
    assert len(res_invalid) == 1
    assert isinstance(res_invalid.get("arg0"), ValidationResult)

def test_or_validator(pipeline: ValidationPipeline):
    pipeline.add_validator("arg0", ORValidator([ValueValidator("jack"), ValueValidator("john")]))

    res_valid = pipeline.validate({"arg0": "john"})

    assert isinstance(res_valid, dict)
    assert len(res_valid) == 0

    res_invalid = pipeline.validate({"arg0": "jaco"})

    assert isinstance(res_invalid, dict)
    assert len(res_invalid) == 1
    assert isinstance(res_invalid.get("arg0"), ValidationResult)

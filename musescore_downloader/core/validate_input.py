from pathvalidate import validate_filepath

from .validation.validation_pipeline import ValidationPipeline
from .validation.choice_validator import ChoiceValidator
from .validation.external_validator import ExternalValidator
from .validation.type_validator import TypeValidator

def validate_path_format(path_format):
    try:
        if "%(title)s" not in path_format:
            raise Exception("The provided directory format does not contain a %(title)s placeholder.")

        validate_filepath(path_format % {'title': "hello_world"})
    except Exception as e:
        return e
    
    return None


def validate_input(
    input_values: dict[str, any]
):
    validator_pipe = ValidationPipeline(
        {
            "url": [TypeValidator(str, required=True)],
            "save_pagefiles": [TypeValidator(bool)],
            "page_size": [ChoiceValidator(["A4", "LETTER"])],
            "dirpath": [TypeValidator(str), ExternalValidator(validate_path_format)]
        }
    )

    result = validator_pipe.validate(input_values)
    return result

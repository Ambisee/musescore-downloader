from pathvalidate import validate_filepath

from ..validation.external_validator import ValidationFunction
from ..validation import (
    ValidationResult,
    ValidationPipeline,
    TypeValidator, 
    ValueValidator,
    ExternalValidator,
    ORValidator,
    ANDValidator,
)

def validate_path_format(path_format: str) -> bool:
    """Validates a path format.
    
    Parameters
    ----------
    path_format : str
        The path string to be validated.

    Returns
    -------
    bool
        True if the path_format is valid, otherwise False.
    """
    try:
        if "%(title)s" not in path_format:
            raise Exception("The provided directory format does not contain a %(title)s placeholder.")

        validate_filepath(path_format % {'title': "hello_world"})
    except Exception as e:
        return False
    
    return True

def validate_input(
    input_values: dict[str, any]
) -> dict[str, ValidationResult]:
    """Validates the configuration values for the scraping process.

    Parameters
    ----------
    input_values : dict
        The collection of key-value pairs representing the configuration values.

    Returns
    -------
    dict
        The dictionary containing configuration keys and the error they encountered.
    """
    validator_pipe = ValidationPipeline(
        {
            "url": TypeValidator(str),
            "save_pagefiles": TypeValidator(bool),
            "page_size": ORValidator([
                ValueValidator("A4"),
                ValueValidator("LETTER")
            ]),
            "dirpath": ORValidator([
                TypeValidator(type(None)),
                ANDValidator([
                    TypeValidator(str),
                    ExternalValidator(
                        ValidationFunction(
                            validate_path_format, 
                            "The value must be a valid pathname with no illegal characters"
                        )
                    )
                ])
            ])
        }
    )

    result = validator_pipe.validate(input_values)
    return result

from pathvalidate import validate_filepath

from .validation import (
    ValidationPipeline,
    TypeValidator, 
    ValueValidator,
    ORValidator,
    ANDValidator,
)

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
            "url": TypeValidator(str),
            "save_pagefiles": TypeValidator(bool),
            "page_size": ORValidator([
                ValueValidator("A4"),
                ValueValidator("LETTER")
            ]),
            "dirpath": ANDValidator([
                TypeValidator(str)
            ])
        }
    )

    result = validator_pipe.validate(input_values)
    return result

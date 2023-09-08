import logging
from musescore_downloader.core.validation.log_errors import log_validation_errors
from musescore_downloader.core.validation import (
    ValidationPipeline,
    ORValidator,
    ANDValidator,
    ValueValidator,
    TypeValidator
)

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


pipe = ValidationPipeline({
    "page_size": ORValidator([ValueValidator("A4"), ValueValidator("LETTER")]),
    "dirpath": ANDValidator([ANDValidator([TypeValidator(str)])])
})

val_res = pipe.validate({
    "page_size": "F4",
    "dirpath": None
})

log_validation_errors(val_res, logging)
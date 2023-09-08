from typing import Literal

from musescore_downloader.core.validation.validation_result import ValidationResult

class BaseValidator:
    """Base Validator Class

    *This class serves as a base class to concrete
    validators. Do not instantiate this class directly.
    """

    def __init__(
        self, 
        validator_value,
    ):
        self.validator_value = validator_value
        self.error = ""
        self.help = ""

        self.build_error()
        self.build_help()

    def build_error(self):
        pass

    def build_help(self):
        pass

    def validate(self, value) -> ValidationResult:
        pass

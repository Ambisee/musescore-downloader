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
        self.error_message = ""
        self.help_message = ""

        self.build_error_message()
        self.build_help_message()

    def build_error_message(self):
        pass

    def build_help_message(self):
        pass

    def validate(self, value) -> ValidationResult:
        pass

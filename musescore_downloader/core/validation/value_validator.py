from musescore_downloader.core.validation.validation_result import ValidationResult
from .validation_result import ValidationResult
from .base_validator import BaseValidator

class ValueValidator(BaseValidator):
    def __init__(
        self,
        valid_value
    ):
        super().__init__(valid_value)

    def build_error_message(self):
        self.error_message = "Received an invalid value: %s"

    def build_help_message(self):
        self.help_message = "Value must be equal to '%s'" % self.validator_value
        
    def validate(self, value) -> ValidationResult:
        status = (value == self.validator_value)

        result = ValidationResult(
            status,
            self.error_message % value,
            self.help_message
        )

        return result
    
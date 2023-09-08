from musescore_downloader.core.validation.validation_result import ValidationResult
from .validator_message import HelpMessage
from . import ValidationResult
from . import BaseValidator

class ValueValidator(BaseValidator):
    def __init__(
        self,
        valid_value
    ):
        super().__init__(valid_value)

    def build_error(self):
        self.error = "Received an invalid value: %s"

    def build_help(self):
        self.help = HelpMessage("Value must be equal to '%s'" % self.validator_value)
        
    def validate(self, value) -> ValidationResult:
        status = (value == self.validator_value)

        result = ValidationResult(
            status,
            self.error % value,
            self.help
        )

        return result
    
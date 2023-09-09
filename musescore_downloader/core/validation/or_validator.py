from musescore_downloader.core.validation.validation_result import ValidationResult
from . import BaseValidator, ValidationResult
from .help import HelpMessageCollection

class ORValidator(BaseValidator):
    def __init__(self, valid_value):
        super().__init__(valid_value)

    def build_error(self):
        self.error = "The input value failed to satisfy one of the conditions."
    
    def build_help(self):
        message = "The input value must fulfill ONE of these requirements:"
        help_messages = []
        
        for validator in self.validator_value:
            help_messages.append(validator.help)
        
        self.help =  HelpMessageCollection(message, help_messages)

    def validate(self, value) -> ValidationResult:
        status = False

        for validator in self.validator_value:
            status = status or validator.validate(value).is_valid()
        
        result = ValidationResult(
            status,
            self.error,
            self.help
        )

        return result

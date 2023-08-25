from musescore_downloader.core.validation.validation_result import ValidationResult
from . import BaseValidator, ValidationResult

class ORValidator(BaseValidator):
    def __init__(self, valid_value):
        super().__init__(valid_value)

    def build_help_message(self):
        self.error_message = "The input value failed to satisfy one of the conditions."
    
    def build_error_message(self):
        self.help_message = "The input value must fulfill ONE of these requirements: \n\t"
        
        for i, validator in enumerate(self.validator_value):
            self.help_message += f"- {validator.help_message}"

            if i < len(self.validator_value) - 1:
                self.help_message += "\n\t"
    
    def validate(self, value) -> ValidationResult:
        status = False

        for validator in self.validator_value:
            status = status or validator.validate(value).is_valid()
        
        result = ValidationResult(
            status,
            self.error_message,
            self.help_message
        )

        return result

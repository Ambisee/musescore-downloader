from . import BaseValidator, ValidationResult

class ExternalValidator(BaseValidator):
    def __init__(
        self, 
        valid_value
    ):
        super().__init__(valid_value)

    def build_error_message(self):
        self.error_message = "External validation failed"

    def build_help_message(self):
        self.help_message = self.validator_value.help_message

    def validate(self, value) -> ValidationResult:
        status = self.validator_value(value)

        result = ValidationResult(
            status,
            self.error_message,
            self.help_message
        )

        return result

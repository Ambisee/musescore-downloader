from .base_validator import BaseValidator
from .validation_result import ValidationResult

class TypeValidator(BaseValidator):
    def __init__(
        self, 
        valid_value: type
    ):
        super().__init__(valid_value)

    def build_error_message(self):
        self.error_message = "Expected variable of type %s, found %s." % (self.validator_value.__name__, "%s")
            
    def build_help_message(self):
        self.help_message = "Variable must be of type: %s" % self.validator_value.__name__

    def validate(self, value):
        status = isinstance(value, self.validator_value)

        result = ValidationResult(
            status,
            self.error_message % type(value),
            self.help_message 
        )

        return result

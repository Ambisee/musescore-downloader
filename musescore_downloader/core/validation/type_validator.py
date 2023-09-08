from .base_validator import BaseValidator
from .validation_result import ValidationResult
from .validator_message import HelpMessage

class TypeValidator(BaseValidator):
    def __init__(
        self, 
        valid_value: type
    ):
        super().__init__(valid_value)

    def build_error(self):
        self.error = "Expected variable of type %s, found %s." % (self.validator_value.__name__, "%s")
            
    def build_help(self):
        self.help = HelpMessage("Variable must be of type: %s" % self.validator_value.__name__)

    def validate(self, value):
        status = isinstance(value, self.validator_value)

        result = ValidationResult(
            status,
            self.error % type(value),
            self.help 
        )

        return result

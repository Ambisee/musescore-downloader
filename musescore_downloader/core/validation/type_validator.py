from .base_validator import BaseValidator
from .validation_result import ValidationResult
from .help import HelpMessage

class TypeValidator(BaseValidator):
    """Validates whether the value type of the input matches a specific type

    This validator checks whether an input is of a specific type. It will fail 
    if the value is of a subtype of the validator type.

    Attributes
    ----------
    validator_value : type
        The object type to test the input value against.
    """
    
    def __init__(
        self, 
        valid_value: type
    ):
        self.validator_value: type
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

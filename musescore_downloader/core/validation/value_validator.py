from typing import Any

from .help import HelpMessage
from . import BaseValidator, ValidationResult


class ValueValidator(BaseValidator):
    """Validates whether the input value is equal to a specified value.
    
    Attributes
    ----------
    validator_value : Any
        The value to be checked against.
    """

    def __init__(
        self,
        valid_value: Any
    ):
        self.validator_value: Any
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
    
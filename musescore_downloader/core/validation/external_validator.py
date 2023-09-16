from typing import Callable, Any

from . import BaseValidator, ValidationResult
from .help import HelpMessage

class ValidationFunction:
    """Validation function class for wrapping a validation function.

    Attributes
    ----------
    val_function : Callable[[Any], bool]
        The validation function to be called with the input value.
    help_message : str
        The instruction on the conditions on the input value.
    error_message : str
        The message when the validation fails on the input.
    """
    
    def __init__(
        self, 
        val_function: Callable[[Any], bool], 
        help_message: str ="", 
        error_message: str ="External validation failed."
    ):
        self.val_function = val_function
        self.help_message = help_message
        self.error_message = error_message

class ExternalValidator(BaseValidator):
    """Validator that uses a given function to validate a value
    
    Attributes
    ----------
    - valid_value : ValidatorFunction
        The object that contains a validator function, and the help and error messages.
        The validator function must accept 1 parameter value and returns a boolean value: True
        if the input is valid and False otherwise.
    """    

    def __init__(
        self, 
        valid_value: ValidationFunction
    ):
        self.validator_value: ValidationFunction
        super().__init__(valid_value)

    def build_error(self):
        self.error = self.validator_value.error_message

    def build_help(self):
        self.help = HelpMessage(self.validator_value.help_message)

    def validate(self, value) -> ValidationResult:
        status = self.validator_value.val_function(value)

        result = ValidationResult(
            status,
            self.error,
            self.help
        )

        return result

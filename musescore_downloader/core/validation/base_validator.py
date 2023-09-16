from typing import Literal, Any

from . import ValidationResult
from .help import HelpMessage

class BaseValidator:
    """Base Validator Class

    *This class serves as a base class to concrete
    validators. Do not instantiate this class directly.

    Attributes
    ----------
    validator_value : Any
        The object that will be test against for input validation.
    error : str
        The error message if the validation process fails.
    help : HelpMessage
        The object containing instructions on what kind of input should be passed.
    """

    def __init__(
        self, 
        validator_value,
    ):
        self.validator_value = validator_value
        self.error = ""
        self.help = HelpMessage("")

        self.build_error()
        self.build_help()

    def build_error(self):
        pass

    def build_help(self):
        pass

    def validate(self, value) -> ValidationResult:
        pass

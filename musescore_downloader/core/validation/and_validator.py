from .base_validator import BaseValidator, ValidationResult
from .help import HelpMessageCollection

class ANDValidator(BaseValidator):
    """Validates whether an input passes through all validator checks in a list of validators.

    Attributes
    ----------
    validator_value : list of BaseValidator
        The list of validators to test the input value against.
    """

    def __init__(
        self, 
        valid_value: list[BaseValidator]
    ):
        self.validator_value: list[BaseValidator]
        super().__init__(valid_value)

    def build_error(self):
        self.error = "The input value failed to satisfy all conditions."

    def build_help(self):
        message = "The input value must fulfill ALL of these requirements:"
        help_messages = []

        for validator in self.validator_value:
            help_messages.append(validator.help)
        
        self.help = HelpMessageCollection(message, help_messages)


    def validate(self, value):
        status = True

        for validator in self.validator_value:
            status = status and validator.validate(value).is_valid()
        
        result = ValidationResult(
            status,
            self.error,
            self.help
        )

        return result

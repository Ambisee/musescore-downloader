from . import BaseValidator, ValidationResult

class ValidationFunction:
    def __init__(self, val_function, help_message="", error_message="External validation failed."):
            self.val_function = val_function
            self.help_message = help_message 
            self.error_message = error_message

class ExternalValidator(BaseValidator):
    """Validator that uses a given function to validate a value
    
    Attributes
    ----------
    - valid_value : any
        A function that will be used to validate a value. The function must have
        a `value` as a parameter and returns a boolean. 

        In addition, the function can also specify a helper text by setting the function's
        `help_message` attribute.
    """
    
    def __init__(
        self, 
        valid_value: ValidationFunction
    ):
        super().__init__(valid_value)

    def build_error(self):
        self.error_message = self.validator_value.error_message

    def build_help(self):
        self.help_message = self.validator_value.help_message

    def validate(self, value) -> ValidationResult:
        status = self.validator_value.val_function(value)

        result = ValidationResult(
            status,
            self.error_message,
            self.help_message
        )

        return result

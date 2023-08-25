from .base_validator import BaseValidator, ValidationResult

class ANDValidator(BaseValidator):
    
    def __init__(
        self, 
        valid_value: list[BaseValidator]
    ):
        super().__init__(valid_value)

    def build_error_message(self):
        self.error_message = "The input value failed to satisfy all conditions."

    def build_help_message(self):
        self.help_message = "The input value must fulfill ALL of these requirements: \n\t"
        
        for i, validator in enumerate(self.validator_value):
            self.help_message += f"- {validator.help_message}"

            if i < len(self.validator_value) - 1:
                self.help_message += "\n\t"

    def validate(self, value):
        status = True

        for validator in self.validator_value:
            status = status and validator.validate(value).is_valid()
        
        result = ValidationResult(
            status,
            self.error_message,
            self.help_message
        )

        return result

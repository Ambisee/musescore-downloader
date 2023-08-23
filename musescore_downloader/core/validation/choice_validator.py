from .base_validator import BaseValidator

class ChoiceValidator(BaseValidator):
    def __init__(
        self, 
        valid_value, 
        required=False, 
        error_message="Expected value to be one of the value from the list : {}."
    ):
        super().__init__(valid_value, required, error_message)

    def validate(self, value):
        requirement_check = super().validate(value)
        if requirement_check is None:
            return None
        
        if value in self.valid_value:
            return None
            
        return ValueError(self.error_message.format(', '.join(self.valid_value)))

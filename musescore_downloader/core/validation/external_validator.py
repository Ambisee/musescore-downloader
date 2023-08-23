from .base_validator import BaseValidator

class ExternalValidator(BaseValidator):
    def __init__(
        self, 
        valid_value, 
        required=False, 
        error_message="An error occured."
    ):
        super().__init__(valid_value, required)

    def validate(self, value):
        requirement_check = super().validate(value)
        
        if requirement_check is None:
            return None
    
        is_valid = self.valid_value(value)
        
        if issubclass(type(is_valid), Exception):
            return is_valid
    
        return None

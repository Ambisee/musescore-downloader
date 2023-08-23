from .base_validator import BaseValidator

class TypeValidator(BaseValidator):
    def __init__(
        self, 
        valid_value: type | list[type], 
        required=False, 
        error_message="Expected variable of type {}, found {}."
    ):
        super().__init__(valid_value, required, error_message)


    def validate(self, value):
        requirement_check = super().validate(value)
        if requirement_check is None:
            return None

        if isinstance(value, self.valid_value):
            return None
        
        return TypeError(self.error_message.format(self.valid_value, type(value)))

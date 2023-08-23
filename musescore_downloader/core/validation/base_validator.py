class BaseValidator:
    """Base Validator Class

    *This class serves as a base class to concrete
    validators. Do not instantiate this class directly.
    """

    def __init__(
        self, 
        valid_value,
        required=False,
        error_message=None,
    ):
        self.valid_value = valid_value
        self.required = required
        self.error_message = error_message

    def validate(self, value):
        if value is None:
            if self.required:
                return ValueError("Required value cannot be None. Please enter a valid value.")
            return None

        return True
class ValidationResult:
    """Validation result class

    This class serves as a shared return value for every concrete
    validator. True if validation is successful and False otherwise. 
    """

    def __init__(
        self,
        status: bool,
        error_message: str,
        help_message: str
    ):
        self.status = status
        self.error_message = error_message
        self.help_message = help_message

    def is_valid(self):
        return self.status

    def get_error(self):
        return self.error_message
    
    def get_help(self):
        return self.help_message

from .validator_message import BaseHelp

class ValidationResult:
    """Validation result class

    This class serves as a shared return value for every concrete
    validator. True if validation is successful and False otherwise. 
    """

    def __init__(
        self,
        status: bool,
        error: str,
        help: BaseHelp
    ):
        self.status = status
        self.error = error
        self.help = help

    def is_valid(self) -> bool:
        return self.status

    def get_error(self) -> str:
        return self.error
    
    def get_help(self) -> BaseHelp:
        return self.help

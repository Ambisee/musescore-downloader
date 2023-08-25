from .base_validator import BaseValidator, ValidationResult

class ValidationPipeline:
    def __init__(
        self, 
        validations=None
    ):
        self.set_validations(validations)

    def set_validations(self, validations):
        if validations is None:
            self.validations: dict[str, BaseValidator] = {}
            return
        
        self.validations = validations

    def add_var(self, var_name):
        self.validations[var_name] = []

    def add_validator(self, var_name, validator):
        self.validations[var_name].append(validator)

    def validate_var(self, var_name, value):
        return self.validations[var_name].validate(value)

    def validate(self, values: dict[str, any]):
        vars = self.validations.keys()
        errors: dict[str, ValidationResult] = {}

        for var in vars:
            res = self.validate_var(var, values[var])
            
            if not res.is_valid():
                errors[var] = res
            
        return errors

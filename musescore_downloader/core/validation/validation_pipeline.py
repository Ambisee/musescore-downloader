from .base_validator import BaseValidator

class ValidationPipeline:
    def __init__(
        self, 
        validations=None
    ):
        self.set_validations(validations)

    def set_validations(self, validations):
        if validations is None:
            self.validations: dict[str, list[BaseValidator]] = {}
        
        self.validations = validations

    def add_var(self, var_name):
        self.validations[var_name] = []

    def add_validator(self, var_name, validator):
        self.validations[var_name].append(validator)

    def validate_var(self, var_name, value):
        result = []
        
        for validator in self.validations[var_name]:
            validator_res = validator.validate(value)
            
            if validator_res is not None:
                result.append(validator_res)
            
        return result

    def validate(self, values: dict[str, any]):
        vars = self.validations.keys()
        errors = {}

        for var in vars:
            res = self.validate_var(var, values[var])
            
            if len(res) > 0:
                errors[var] = res
            
        return errors

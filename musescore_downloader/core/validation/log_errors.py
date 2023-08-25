from . import ValidationResult

def log_validation_errors(error: dict[str, ValidationResult], logger):
    logger.error("An error occured during the process of input validation.\n")
    for k in error.keys():
        print(f"- {k} : {error[k].get_error()} \n")
        print(error[k].get_help(), '\n')
    
    return

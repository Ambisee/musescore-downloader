class UninitializedWebDriverError(Exception):
    """No webdriver initialized."""

class InitialElementNotFoundError(Exception):
    """Unable to find the initial element."""

class PageElementNotFoundError(Exception):
    """Unable to retrieve the next page element."""

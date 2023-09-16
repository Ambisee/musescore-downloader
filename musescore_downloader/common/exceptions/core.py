class InvalidURLError(Exception):
    """Invalid web URL was provided."""

class InvalidContentTypeError(Exception):
    """Unrecognized content type of a page's content."""

class NoConnectionError(Exception):
    """The user is offline."""

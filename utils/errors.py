class InvalidDID(Exception):
    """Raised when a DID string is malformed or cannot be parsed."""
    pass

class MissingAxisError(Exception):
    """Raised when axis code not found in metadata."""
    pass

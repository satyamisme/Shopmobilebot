class ProductNotFoundError(Exception):
    """Raised when a product is not found in the database."""
    pass

class InvalidUpdateError(Exception):
    """Raised when an invalid product update is attempted."""
    pass

class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass

class TransferError(Exception):
    """Raised when a transfer operation fails."""
    pass

class ShopNotFoundError(Exception):
    """Raised when a shop is not found."""
    pass
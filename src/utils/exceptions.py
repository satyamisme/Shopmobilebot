class InventoryError(Exception):
    """Base exception for inventory-related errors"""
    pass

class DataError(InventoryError):
    """Raised when there are issues with data operations"""
    pass

class ProductNotFoundError(InventoryError):
    """Raised when a product is not found"""
    pass

class InvalidDataError(InventoryError):
    """Raised when data validation fails"""
    pass

class ExcelError(InventoryError):
    """Raised when there are issues with Excel operations"""
    pass
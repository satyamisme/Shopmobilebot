from typing import Dict, Any
import re
from .exceptions import InvalidDataError

class DataValidator:
    @staticmethod
    def validate_query(query: str) -> str:
        """Validate and sanitize search query"""
        if not query or len(query.strip()) < 2:
            raise InvalidDataError("Query must be at least 2 characters long")
        return re.sub(r'[<>"/\\&;]', '', query.strip())
    
    @staticmethod
    def validate_product_id(product_id: Any) -> int:
        """Validate product ID"""
        try:
            pid = int(product_id)
            if pid <= 0:
                raise InvalidDataError("Product ID must be positive")
            return pid
        except (ValueError, TypeError):
            raise InvalidDataError("Invalid product ID format")
    
    @staticmethod
    def validate_stock_update(stock: Any) -> int:
        """Validate stock update value"""
        try:
            stock_val = int(stock)
            if stock_val < 0:
                raise InvalidDataError("Stock cannot be negative")
            return stock_val
        except (ValueError, TypeError):
            raise InvalidDataError("Invalid stock value")
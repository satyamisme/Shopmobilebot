from typing import List
from ..models import Product
from collections import defaultdict

class InventoryAnalytics:
    @staticmethod
    def get_stock_summary(products: List[Product]) -> dict:
        """Get summary of stock levels"""
        total = len(products)
        in_stock = sum(1 for p in products if p.is_in_stock)
        out_of_stock = total - in_stock
        low_stock = sum(1 for p in products if 0 < p.stock <= 5)
        
        return {
            'total': total,
            'in_stock': in_stock,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'stock_rate': (in_stock / total * 100) if total > 0 else 0
        }
    
    @staticmethod
    def get_price_analytics(products: List[Product]) -> dict:
        """Get price statistics"""
        if not products:
            return {}
            
        prices = [p.price for p in products]
        return {
            'avg_price': sum(prices) / len(prices),
            'min_price': min(prices),
            'max_price': max(prices)
        }
    
    @staticmethod
    def get_model_distribution(products: List[Product]) -> dict:
        """Get distribution of products by model"""
        model_count = defaultdict(int)
        for product in products:
            base_model = product.model.split()[0]  # Get brand name
            model_count[base_model] += 1
        return dict(model_count)
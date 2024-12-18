from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, excel_path: str = 'data/products.xlsx'):
        self.excel_path = excel_path
    
    def get_inventory_summary(self) -> Dict:
        """Get summary of current inventory"""
        df = pd.read_excel(self.excel_path)
        
        total = len(df)
        in_stock = len(df[df['Status'] == 'in_stock'])
        
        return {
            'total_products': total,
            'in_stock': in_stock,
            'out_of_stock': total - in_stock,
            'stock_rate': round((in_stock / total * 100), 2) if total > 0 else 0
        }
    
    def get_shop_statistics(self) -> List[Dict]:
        """Get statistics for each shop"""
        df = pd.read_excel(self.excel_path)
        stats = []
        
        for shop_id in df['Shop_ID'].unique():
            shop_df = df[df['Shop_ID'] == shop_id]
            stats.append({
                'shop_id': shop_id,
                'total_products': len(shop_df),
                'in_stock': len(shop_df[shop_df['Status'] == 'in_stock']),
                'models': shop_df['Model'].nunique()
            })
        
        return stats
    
    def get_model_distribution(self) -> Dict[str, int]:
        """Get distribution of products by model"""
        df = pd.read_excel(self.excel_path)
        return df['Model'].value_counts().to_dict()
    
    def get_price_analytics(self) -> Dict:
        """Get price statistics"""
        df = pd.read_excel(self.excel_path)
        prices = df['Price'].dropna()
        
        return {
            'average_price': round(prices.mean(), 2),
            'min_price': prices.min(),
            'max_price': prices.max(),
            'median_price': prices.median()
        }
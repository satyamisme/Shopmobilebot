import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
from .exceptions import DataError, ProductNotFoundError
from .validators import DataValidator
from .logger import setup_logger

logger = setup_logger()

class DataManager:
    def __init__(self, excel_path: str = 'data/products.xlsx'):
        self.excel_path = excel_path
        try:
            self.df = pd.read_excel(excel_path)
            logger.info(f"Loaded {len(self.df)} products from {excel_path}")
        except Exception as e:
            logger.error(f"Failed to load Excel file: {str(e)}")
            raise DataError(f"Could not load data: {str(e)}")

    def search_products(self, query: str) -> List[Dict]:
        """Search products by any field"""
        try:
            query = DataValidator.validate_query(query)
            df_lower = self.df.astype(str).apply(lambda x: x.str.lower())
            mask = df_lower.apply(lambda x: x.str.contains(query, na=False)).any(axis=1)
            results = self.df[mask].to_dict('records')
            logger.info(f"Found {len(results)} products matching '{query}'")
            return results
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise DataError(f"Search failed: {str(e)}")

    def get_product_by_id(self, product_id: int) -> Dict:
        """Get product by ID"""
        try:
            product_id = DataValidator.validate_product_id(product_id)
            product = self.df[self.df['ID'] == product_id]
            if product.empty:
                raise ProductNotFoundError(f"Product with ID {product_id} not found")
            return product.to_dict('records')[0]
        except ProductNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get product: {str(e)}")
            raise DataError(f"Failed to get product: {str(e)}")

    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """Update product stock"""
        try:
            product_id = DataValidator.validate_product_id(product_id)
            new_stock = DataValidator.validate_stock_update(new_stock)
            
            mask = self.df['ID'] == product_id
            if not mask.any():
                raise ProductNotFoundError(f"Product with ID {product_id} not found")
            
            self.df.loc[mask, 'Stock'] = new_stock
            self.df.loc[mask, 'LastUpdated'] = datetime.now().isoformat()
            self.df.to_excel(self.excel_path, index=False)
            
            logger.info(f"Updated stock for product {product_id} to {new_stock}")
            return True
        except Exception as e:
            logger.error(f"Stock update failed: {str(e)}")
            raise DataError(f"Stock update failed: {str(e)}")

    def get_low_stock_products(self, threshold: int = 5) -> List[Dict]:
        """Get products with low stock"""
        try:
            threshold = DataValidator.validate_stock_update(threshold)
            low_stock = self.df[self.df['Stock'] <= threshold]
            logger.info(f"Found {len(low_stock)} products with stock <= {threshold}")
            return low_stock.to_dict('records')
        except Exception as e:
            logger.error(f"Failed to get low stock products: {str(e)}")
            raise DataError(f"Failed to get low stock products: {str(e)}")

    def refresh_data(self):
        """Reload data from Excel file"""
        try:
            self.df = pd.read_excel(self.excel_path)
            logger.info(f"Refreshed data from {self.excel_path}")
        except Exception as e:
            logger.error(f"Failed to refresh data: {str(e)}")
            raise DataError(f"Failed to refresh data: {str(e)}")
from typing import List, Dict
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product, Shop
from utils.logger import logger

class DataSyncService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def sync_from_excel(self, file_path: str = 'data/products.xlsx'):
        """Sync database with Excel data"""
        try:
            df = pd.read_excel(file_path)
            products = df.to_dict('records')
            
            async with self.session.begin():
                for product_data in products:
                    product = await self._get_or_create_product(product_data)
                    await self._update_product(product, product_data)
            
            logger.info(f"Successfully synced {len(products)} products from Excel")
        except Exception as e:
            logger.error(f"Error syncing data: {str(e)}")
            raise
    
    async def _get_or_create_product(self, data: Dict) -> Product:
        stmt = select(Product).where(Product.imei == data['IMEI'])
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        
        if not product:
            product = Product(imei=data['IMEI'])
            self.session.add(product)
        
        return product
    
    async def _update_product(self, product: Product, data: Dict):
        product.model = data['Model']
        product.ram = data.get('RAM')
        product.storage = data.get('Storage')
        product.network = data.get('Network')
        product.price = float(data['Price'])
        product.condition = data.get('Condition', 'new')
        product.status = data.get('Status', 'in_stock')
        product.shop_id = int(data.get('Shop_ID', 1))
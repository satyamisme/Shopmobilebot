from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Product
import pandas as pd
from typing import List, Dict
from src.config import settings

class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all_products(self) -> List[Product]:
        stmt = select(Product)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search_products(self, query: str) -> List[Product]:
        query = query.lower()
        stmt = select(Product).where(
            (Product.model.ilike(f"%{query}%")) |
            (Product.ram.ilike(f"%{query}%")) |
            (Product.network.ilike(f"%{query}%")) |
            (Product.storage.ilike(f"%{query}%"))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def sync_from_excel(self):
        try:
            df = pd.read_excel(settings.EXCEL_FILE_PATH)
            products = df.to_dict('records')
            
            for product_data in products:
                stmt = select(Product).where(Product.imei == str(product_data['IMEI']))
                result = await self.session.execute(stmt)
                product = result.scalar_one_or_none()
                
                if product:
                    # Update existing product
                    for key, value in product_data.items():
                        if hasattr(product, key.lower()):
                            setattr(product, key.lower(), value)
                else:
                    # Create new product
                    new_product = Product(
                        imei=str(product_data['IMEI']),
                        model=product_data['Model'],
                        ram=product_data.get('RAM', ''),
                        storage=product_data.get('Storage', ''),
                        network=product_data.get('Network', ''),
                        price=float(product_data['Price']),
                        condition=product_data.get('Condition', 'new'),
                        status=product_data.get('Status', 'in_stock')
                    )
                    self.session.add(new_product)
            
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
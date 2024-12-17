from typing import Dict, Optional, Tuple
import pandas as pd
from datetime import datetime

class TransferService:
    def __init__(self, excel_path: str = 'data/products.xlsx'):
        self.excel_path = excel_path
        self.transfers_df = self._load_transfers()
    
    def _load_transfers(self) -> pd.DataFrame:
        """Load or create transfers tracking DataFrame"""
        try:
            return pd.read_excel('data/transfers.xlsx')
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                'ID', 'Product_IMEI', 'From_Shop', 'To_Shop',
                'Status', 'Initiated_By', 'Transfer_Date',
                'Completed_Date', 'Notes'
            ])
            df.to_excel('data/transfers.xlsx', index=False)
            return df
    
    def transfer_product(self, product_imei: str, from_shop: int, 
                        to_shop: int, initiated_by: int) -> Tuple[bool, str]:
        """Process a product transfer between shops"""
        try:
            # Load current product data
            products_df = pd.read_excel(self.excel_path)
            
            # Verify product exists and is in source shop
            product_mask = (products_df['IMEI'] == product_imei) & \
                         (products_df['Shop_ID'] == from_shop)
            
            if not product_mask.any():
                return False, "Product not found in source shop"
            
            # Create transfer record
            transfer_id = len(self.transfers_df) + 1
            transfer_record = {
                'ID': transfer_id,
                'Product_IMEI': product_imei,
                'From_Shop': from_shop,
                'To_Shop': to_shop,
                'Status': 'completed',
                'Initiated_By': initiated_by,
                'Transfer_Date': datetime.now().isoformat(),
                'Completed_Date': datetime.now().isoformat(),
                'Notes': f'Transfer from Shop {from_shop} to Shop {to_shop}'
            }
            
            # Update product location
            products_df.loc[product_mask, 'Shop_ID'] = to_shop
            
            # Save changes
            products_df.to_excel(self.excel_path, index=False)
            self.transfers_df = pd.concat([
                self.transfers_df,
                pd.DataFrame([transfer_record])
            ], ignore_index=True)
            self.transfers_df.to_excel('data/transfers.xlsx', index=False)
            
            return True, f"Product transferred successfully from Shop {from_shop} to Shop {to_shop}"
            
        except Exception as e:
            return False, f"Transfer failed: {str(e)}"
    
    def get_transfer_history(self, product_imei: Optional[str] = None,
                           shop_id: Optional[int] = None) -> pd.DataFrame:
        """Get transfer history with optional filters"""
        df = self.transfers_df
        
        if product_imei:
            df = df[df['Product_IMEI'] == product_imei]
        
        if shop_id:
            df = df[(df['From_Shop'] == shop_id) | (df['To_Shop'] == shop_id)]
            
        return df.sort_values('Transfer_Date', ascending=False)
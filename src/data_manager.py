import pandas as pd
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
from .models import Device, Purchase, Return, UsedDevicePurchase, Shop
from .exceptions import (
    DeviceNotFoundError, 
    InvalidUpdateError, 
    TransferError,
    ReturnError
)

class DataManager:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self._devices_df = None
        self._shops_df = None
        self._purchases_df = None
        self._returns_df = None
        self._used_purchases_df = None
        self.refresh_data()

    def refresh_data(self):
        """Reload all data from Excel files"""
        self._devices_df = pd.read_excel(f"{self.data_dir}/devices.xlsx")
        self._shops_df = pd.read_excel(f"{self.data_dir}/shops.xlsx")
        self._purchases_df = pd.read_excel(f"{self.data_dir}/purchases.xlsx")
        self._returns_df = pd.read_excel(f"{self.data_dir}/returns.xlsx")
        self._used_purchases_df = pd.read_excel(f"{self.data_dir}/used_purchases.xlsx")

    def save_data(self):
        """Save all current data to Excel files"""
        self._devices_df.to_excel(f"{self.data_dir}/devices.xlsx", index=False)
        self._shops_df.to_excel(f"{self.data_dir}/shops.xlsx", index=False)
        self._purchases_df.to_excel(f"{self.data_dir}/purchases.xlsx", index=False)
        self._returns_df.to_excel(f"{self.data_dir}/returns.xlsx", index=False)
        self._used_purchases_df.to_excel(f"{self.data_dir}/used_purchases.xlsx", index=False)

    def get_device_by_imei(self, imei: str) -> Optional[Device]:
        """Get device details by IMEI"""
        mask = self._devices_df['IMEI'] == imei
        if not mask.any():
            return None
        return Device.from_dict(self._devices_df[mask].iloc[0])

    def search_devices(self, query: str, shop_id: Optional[int] = None,
                      condition: Optional[str] = None) -> List[Device]:
        """Search devices by any field with optional filters"""
        query = str(query).lower()
        df = self._devices_df
        
        if shop_id is not None:
            df = df[df['Shop_ID'] == shop_id]
        
        if condition is not None:
            df = df[df['Condition'] == condition]
        
        results = []
        for _, row in df.iterrows():
            if any(query in str(value).lower() for value in row):
                results.append(Device.from_dict(row))
        
        return results

    def record_purchase(self, device_imei: str, customer_name: str,
                       customer_phone: str, shop_id: int,
                       payment_method: str, notes: Optional[str] = None) -> Purchase:
        """Record a new device purchase"""
        device = self.get_device_by_imei(device_imei)
        if not device:
            raise DeviceNotFoundError(f"Device with IMEI {device_imei} not found")
        
        if device.status != 'in_stock':
            raise InvalidUpdateError(f"Device is not available for sale (status: {device.status})")
        
        # Create purchase record
        purchase_id = len(self._purchases_df) + 1
        purchase_date = datetime.now()
        purchase = Purchase(
            id=purchase_id,
            device_imei=device_imei,
            customer_name=customer_name,
            customer_phone=customer_phone,
            purchase_price=device.price,
            purchase_date=purchase_date,
            shop_id=shop_id,
            payment_method=payment_method,
            warranty_period=365,  # Default 1-year warranty
            notes=notes
        )
        
        # Update device status
        mask = self._devices_df['IMEI'] == device_imei
        self._devices_df.loc[mask, 'Status'] = 'sold'
        self._devices_df.loc[mask, 'Purchase_Date'] = purchase_date.isoformat()
        self._devices_df.loc[mask, 'Warranty_End'] = (purchase_date + timedelta(days=365)).isoformat()
        
        # Add purchase record
        self._purchases_df = pd.concat([
            self._purchases_df,
            pd.DataFrame([purchase.to_dict()])
        ], ignore_index=True)
        
        self.save_data()
        return purchase

    def process_return(self, purchase_id: int, reason: str,
                      condition: str, processed_by: str,
                      notes: Optional[str] = None) -> Return:
        """Process a device return"""
        # Verify purchase exists and is within return period
        purchase_mask = self._purchases_df['ID'] == purchase_id
        if not purchase_mask.any():
            raise ReturnError("Purchase not found")
        
        purchase_data = self._purchases_df[purchase_mask].iloc[0]
        purchase_date = datetime.fromisoformat(purchase_data['Purchase_Date'])
        
        if datetime.now() - purchase_date > timedelta(days=3):
            raise ReturnError("Return period (3 days) has expired")
        
        # Create return record
        return_id = len(self._returns_df) + 1
        return_record = Return(
            id=return_id,
            purchase_id=purchase_id,
            return_date=datetime.now(),
            reason=reason,
            condition=condition,
            refund_amount=float(purchase_data['Purchase_Price']),
            status='pending',
            processed_by=processed_by,
            notes=notes
        )
        
        # Update device status
        device_mask = self._devices_df['IMEI'] == purchase_data['Device_IMEI']
        self._devices_df.loc[device_mask, 'Status'] = 'returned'
        
        # Add return record
        self._returns_df = pd.concat([
            self._returns_df,
            pd.DataFrame([return_record.to_dict()])
        ], ignore_index=True)
        
        self.save_data()
        return return_record

    def purchase_used_device(self, imei: str, serial_number: str,
                           model: str, seller_info: Dict[str, str],
                           condition: str, price: float,
                           shop_id: int, processed_by: str,
                           notes: Optional[str] = None) -> Tuple[Device, UsedDevicePurchase]:
        """Record purchase of a used device"""
        # Create device record
        device = Device(
            imei=imei,
            serial_number=serial_number,
            model=model,
            ram=seller_info.get('ram', 'Unknown'),
            network=seller_info.get('network', 'Unknown'),
            price=price * 1.3,  # 30% markup
            condition='used',
            shop_id=shop_id,
            status='in_stock',
            purchase_date=datetime.now(),
            warranty_end=None
        )
        
        # Create used purchase record
        purchase_id = len(self._used_purchases_df) + 1
        used_purchase = UsedDevicePurchase(
            id=purchase_id,
            device_imei=imei,
            seller_name=seller_info['name'],
            seller_phone=seller_info['phone'],
            purchase_price=price,
            purchase_date=datetime.now(),
            condition=condition,
            verified_status=True,
            shop_id=shop_id,
            processed_by=processed_by,
            notes=notes
        )
        
        # Add records to DataFrames
        self._devices_df = pd.concat([
            self._devices_df,
            pd.DataFrame([device.to_dict()])
        ], ignore_index=True)
        
        self._used_purchases_df = pd.concat([
            self._used_purchases_df,
            pd.DataFrame([used_purchase.to_dict()])
        ], ignore_index=True)
        
        self.save_data()
        return device, used_purchase

    def get_device_history(self, imei: str) -> Dict[str, List]:
        """Get complete history of a device"""
        device = self.get_device_by_imei(imei)
        if not device:
            raise DeviceNotFoundError(f"Device with IMEI {imei} not found")
        
        # Get purchase history
        purchases = self._purchases_df[self._purchases_df['Device_IMEI'] == imei]
        purchase_ids = purchases['ID'].tolist()
        
        # Get returns for these purchases
        returns = self._returns_df[self._returns_df['Purchase_ID'].isin(purchase_ids)]
        
        # Get used purchase history
        used_purchases = self._used_purchases_df[self._used_purchases_df['Device_IMEI'] == imei]
        
        return {
            'device': device.to_dict(),
            'purchases': purchases.to_dict('records'),
            'returns': returns.to_dict('records'),
            'used_purchases': used_purchases.to_dict('records')
        }
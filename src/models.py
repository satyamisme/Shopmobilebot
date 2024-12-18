from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Shop:
    id: int
    name: str
    location: str
    is_warehouse: bool = False

@dataclass
class Device:
    imei: str
    serial_number: str
    model: str
    ram: str
    network: str
    price: float
    condition: str  # new, used, refurbished
    shop_id: int
    status: str  # in_stock, sold, returned, transferred
    purchase_date: Optional[datetime] = None
    warranty_end: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'imei': self.imei,
            'serial_number': self.serial_number,
            'model': self.model,
            'ram': self.ram,
            'network': self.network,
            'price': self.price,
            'condition': self.condition,
            'shop_id': self.shop_id,
            'status': self.status,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'warranty_end': self.warranty_end.isoformat() if self.warranty_end else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Device':
        return cls(
            imei=str(data['IMEI']),
            serial_number=str(data['Serial_Number']),
            model=str(data['Model']),
            ram=str(data['RAM']),
            network=str(data['Network']),
            price=float(data['Price']),
            condition=str(data['Condition']),
            shop_id=int(data['Shop_ID']),
            status=str(data['Status']),
            purchase_date=datetime.fromisoformat(data['Purchase_Date']) if data.get('Purchase_Date') else None,
            warranty_end=datetime.fromisoformat(data['Warranty_End']) if data.get('Warranty_End') else None
        )

@dataclass
class Purchase:
    id: int
    device_imei: str
    customer_name: str
    customer_phone: str
    purchase_price: float
    purchase_date: datetime
    shop_id: int
    payment_method: str
    warranty_period: int  # in days
    notes: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_imei': self.device_imei,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat(),
            'shop_id': self.shop_id,
            'payment_method': self.payment_method,
            'warranty_period': self.warranty_period,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Purchase':
        return cls(
            id=int(data['ID']),
            device_imei=str(data['Device_IMEI']),
            customer_name=str(data['Customer_Name']),
            customer_phone=str(data['Customer_Phone']),
            purchase_price=float(data['Purchase_Price']),
            purchase_date=datetime.fromisoformat(data['Purchase_Date']),
            shop_id=int(data['Shop_ID']),
            payment_method=str(data['Payment_Method']),
            warranty_period=int(data['Warranty_Period']),
            notes=data.get('Notes')
        )

@dataclass
class Return:
    id: int
    purchase_id: int
    return_date: datetime
    reason: str
    condition: str
    refund_amount: float
    status: str  # pending, approved, rejected, completed
    processed_by: str
    notes: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'purchase_id': self.purchase_id,
            'return_date': self.return_date.isoformat(),
            'reason': self.reason,
            'condition': self.condition,
            'refund_amount': self.refund_amount,
            'status': self.status,
            'processed_by': self.processed_by,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Return':
        return cls(
            id=int(data['ID']),
            purchase_id=int(data['Purchase_ID']),
            return_date=datetime.fromisoformat(data['Return_Date']),
            reason=str(data['Reason']),
            condition=str(data['Condition']),
            refund_amount=float(data['Refund_Amount']),
            status=str(data['Status']),
            processed_by=str(data['Processed_By']),
            notes=data.get('Notes')
        )

@dataclass
class UsedDevicePurchase:
    id: int
    device_imei: str
    seller_name: str
    seller_phone: str
    purchase_price: float
    purchase_date: datetime
    condition: str
    verified_status: bool
    shop_id: int
    processed_by: str
    notes: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_imei': self.device_imei,
            'seller_name': self.seller_name,
            'seller_phone': self.seller_phone,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat(),
            'condition': self.condition,
            'verified_status': self.verified_status,
            'shop_id': self.shop_id,
            'processed_by': self.processed_by,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UsedDevicePurchase':
        return cls(
            id=int(data['ID']),
            device_imei=str(data['Device_IMEI']),
            seller_name=str(data['Seller_Name']),
            seller_phone=str(data['Seller_Phone']),
            purchase_price=float(data['Purchase_Price']),
            purchase_date=datetime.fromisoformat(data['Purchase_Date']),
            condition=str(data['Condition']),
            verified_status=bool(data['Verified_Status']),
            shop_id=int(data['Shop_ID']),
            processed_by=str(data['Processed_By']),
            notes=data.get('Notes')
        )
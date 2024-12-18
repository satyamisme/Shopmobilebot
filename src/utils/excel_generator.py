import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Dict, List

class MobileDataGenerator:
    def __init__(self):
        self.brands = ['iPhone', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'OPPO', 'Vivo']
        self.models = {
            'iPhone': ['13 Pro Max', '13 Pro', '13', '12 Pro Max', '12 Pro', '12'],
            'Samsung': ['S23 Ultra', 'S23+', 'S23', 'S22 Ultra', 'S22+', 'S22'],
            'Google': ['Pixel 7 Pro', 'Pixel 7', 'Pixel 6 Pro', 'Pixel 6'],
            'OnePlus': ['11', '10 Pro', '10T', '9 Pro', '9'],
            'Xiaomi': ['13 Pro', '13', '12 Pro', '12', 'Poco F5'],
            'OPPO': ['Find X6 Pro', 'Find X6', 'Reno 8 Pro'],
            'Vivo': ['X90 Pro', 'X90', 'V27 Pro']
        }
        self.ram_options = ['4GB', '6GB', '8GB', '12GB', '16GB']
        self.storage_options = ['64GB', '128GB', '256GB', '512GB', '1TB']
        self.colors = ['Black', 'White', 'Gold', 'Silver', 'Blue', 'Red']
        self.conditions = ['New', 'Like New', 'Used', 'Refurbished']

    def _get_display_specs(self, brand: str, model: str) -> str:
        if brand == 'iPhone':
            return '6.7" OLED 120Hz' if 'Pro' in model else '6.1" OLED 60Hz'
        elif brand == 'Samsung':
            return '6.8" AMOLED 120Hz' if 'Ultra' in model else '6.6" AMOLED 120Hz'
        return '6.5" AMOLED 120Hz'

    def _get_camera_specs(self, brand: str, model: str) -> str:
        if brand == 'iPhone' and 'Pro' in model:
            return '48MP+12MP+12MP'
        elif brand == 'Samsung' and 'Ultra' in model:
            return '108MP+12MP+10MP+10MP'
        return '50MP+12MP+12MP'

    def _generate_imei(self) -> str:
        return ''.join([str(np.random.randint(0, 9)) for _ in range(15)])

    def _generate_serial(self, brand: str) -> str:
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return f"{brand[:3].upper()}{''.join(np.random.choice(list(chars)) for _ in range(7))}"

    def generate_data(self) -> pd.DataFrame:
        products = []
        product_id = 1

        for brand in self.brands:
            for model in self.models[brand]:
                for ram in self.ram_options:
                    for storage in self.storage_options:
                        ram_val = int(ram.replace('GB', ''))
                        storage_val = int(storage.replace('GB', '').replace('TB', '000'))
                        
                        if ram_val <= storage_val and storage_val >= ram_val * 8:
                            base_price = np.random.randint(300, 1500)
                            is_new = '13' in model or '23' in model or '7' in model
                            
                            products.append({
                                'ID': product_id,
                                'Brand': brand,
                                'Model': f"{brand} {model}",
                                'RAM': ram,
                                'Storage': storage,
                                'Network': '5G' if is_new else np.random.choice(['4G', '5G']),
                                'Display': self._get_display_specs(brand, model),
                                'Camera': self._get_camera_specs(brand, model),
                                'Color': np.random.choice(self.colors),
                                'Condition': np.random.choice(self.conditions),
                                'Price': base_price + (ram_val * 50) + (storage_val * 0.5),
                                'Stock': np.random.randint(0, 10),
                                'IMEI': self._generate_imei(),
                                'Serial': self._generate_serial(brand),
                                'LastUpdated': datetime.now().isoformat()
                            })
                            product_id += 1

        return pd.DataFrame(products)

    def save_excel(self, output_path: str = 'data/products.xlsx'):
        os.makedirs('data', exist_ok=True)
        df = self.generate_data()
        df.to_excel(output_path, index=False)
        print(f"Sample data has been generated in {output_path}")

if __name__ == "__main__":
    generator = MobileDataGenerator()
    generator.save_excel()
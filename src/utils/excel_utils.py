import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def read_excel(self, filename: str) -> pd.DataFrame:
        """Read Excel file safely"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            return pd.read_excel(filepath)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return pd.DataFrame()
    
    def write_excel(self, df: pd.DataFrame, filename: str) -> bool:
        """Write DataFrame to Excel safely"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            df.to_excel(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            return False
    
    def append_to_excel(self, data: Dict, filename: str) -> bool:
        """Append new data to existing Excel file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            df = pd.read_excel(filepath) if os.path.exists(filepath) else pd.DataFrame()
            new_df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            return self.write_excel(new_df, filename)
        except Exception as e:
            print(f"Error appending to {filename}: {e}")
            return False
    
    def backup_excel(self, filename: str) -> bool:
        """Create backup of Excel file"""
        try:
            source = os.path.join(self.data_dir, filename)
            if not os.path.exists(source):
                return False
                
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(self.data_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = f"{os.path.splitext(filename)[0]}_{timestamp}.xlsx"
            backup_path = os.path.join(backup_dir, backup_file)
            
            df = pd.read_excel(source)
            df.to_excel(backup_path, index=False)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
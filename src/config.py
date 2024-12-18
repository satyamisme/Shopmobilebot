#from pydantic import BaseSettings
from pydantic_settings import BaseSettings

from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Bot Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///data/inventory.db')
    
    # Web Interface
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', 'admin')
    
    # User Management
    ADMIN_IDS: List[int] = [int(id_) for id_ in os.getenv('ADMIN_IDS', '').split(',') if id_.strip().isdigit()]
    POWER_USER_IDS: List[int] = [int(id_) for id_ in os.getenv('POWER_USER_IDS', '').split(',') if id_.strip().isdigit()]
    
    # Permissions
    ADMIN_PERMISSIONS: List[str] = os.getenv('ADMIN_PERMISSIONS', 'all').split(',')
    POWER_USER_PERMISSIONS: List[str] = os.getenv('POWER_USER_PERMISSIONS', 'search,refresh,transfer').split(',')
    USER_PERMISSIONS: List[str] = os.getenv('USER_PERMISSIONS', 'search').split(',')
    
    # Excel Configuration
    EXCEL_FILE_PATH: str = os.getenv('EXCEL_FILE_PATH', 'data/products.xlsx')
    
    class Config:
        case_sensitive = True

settings = Settings()
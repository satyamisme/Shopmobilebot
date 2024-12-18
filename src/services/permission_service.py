from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class PermissionService:
    def __init__(self):
        self.admin_ids = self._parse_ids(os.getenv('ADMIN_IDS', ''))
        self.power_user_ids = self._parse_ids(os.getenv('POWER_USER_IDS', ''))
        
        self.admin_permissions = set(os.getenv('ADMIN_PERMISSIONS', 'all').split(','))
        self.power_user_permissions = set(os.getenv('POWER_USER_PERMISSIONS', '').split(','))
        self.user_permissions = set(os.getenv('USER_PERMISSIONS', 'search').split(','))
    
    def _parse_ids(self, ids_str: str) -> List[int]:
        """Convert comma-separated ID string to list of integers"""
        return [int(id_) for id_ in ids_str.split(',') if id_.strip().isdigit()]
    
    def get_user_role(self, user_id: int) -> str:
        """Get user's role based on their ID"""
        if user_id in self.admin_ids:
            return 'admin'
        elif user_id in self.power_user_ids:
            return 'power_user'
        return 'user'
    
    def check_permission(self, user_id: int, permission: str) -> bool:
        """Check if user has specific permission"""
        role = self.get_user_role(user_id)
        
        if role == 'admin':
            return True
        elif role == 'power_user':
            return permission in self.power_user_permissions
        else:
            return permission in self.user_permissions
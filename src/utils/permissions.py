from typing import List, Set
import os
from dotenv import load_dotenv

load_dotenv()

class Permissions:
    def __init__(self):
        self.admin_ids = self._parse_ids(os.getenv('ADMIN_IDS', ''))
        self.power_user_ids = self._parse_ids(os.getenv('POWER_USER_IDS', ''))
        
        # Define default permissions for each role
        self.role_permissions = {
            'admin': {
                'search', 'refresh', 'update', 'transfer', 'view_stats',
                'manage_users', 'view_history', 'export_data'
            },
            'power_user': {'search', 'refresh', 'transfer', 'view_stats'},
            'user': {'search'}
        }
    
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
    
    def get_role_permissions(self, role: str) -> Set[str]:
        """Get permissions for a specific role"""
        return self.role_permissions.get(role, set())
    
    def check_permission(self, user_id: int, permission: str) -> bool:
        """Check if user has specific permission"""
        role = self.get_user_role(user_id)
        return permission in self.get_role_permissions(role)
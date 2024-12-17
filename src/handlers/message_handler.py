from telegram import Update
from telegram.ext import ContextTypes
from services.product_service import ProductService
from services.permission_service import PermissionService
from utils.formatters import format_product_details

class MessageHandler:
    def __init__(self, product_service: ProductService, permission_service: PermissionService):
        self.product_service = product_service
        self.permission_service = permission_service
    
    async def handle_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle search queries"""
        user_id = update.effective_user.id
        
        if not self.permission_service.check_permission(user_id, 'search'):
            await update.message.reply_text('⛔ You do not have permission to search products.')
            return
        
        query = update.message.text
        products = self.product_service.search_products(query)
        
        if products:
            # Send each product as a separate message
            for product in products:
                formatted_msg = format_product_details(product)
                await update.message.reply_text(formatted_msg, parse_mode='Markdown')
                
            if len(products) > 1:
                await update.message.reply_text(f'Found {len(products)} matching products.')
        else:
            await update.message.reply_text('No products found matching your search. Please try a different term.')
from telegram import Update
from telegram.ext import ContextTypes
from services.product_service import ProductService
from services.permission_service import PermissionService
from services.transfer_service import TransferService
from services.analytics_service import AnalyticsService
from utils.formatters import format_help_message, format_product_details
from handlers.stats_handler import StatsHandler

class CommandHandler:
    def __init__(self, product_service: ProductService, 
                 permission_service: PermissionService):
        self.product_service = product_service
        self.permission_service = permission_service
        self.transfer_service = TransferService()
        self.analytics_service = AnalyticsService()
        self.stats_handler = StatsHandler(self.analytics_service, permission_service)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        role = self.permission_service.get_user_role(user_id)
        
        welcome_msg = format_help_message(role)
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        role = self.permission_service.get_user_role(user_id)
        
        help_msg = format_help_message(role)
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def refresh_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /refresh command"""
        user_id = update.effective_user.id
        
        if not self.permission_service.check_permission(user_id, 'refresh'):
            await update.message.reply_text('⛔ You do not have permission to use this command.')
            return
        
        self.product_service.refresh_data()
        await update.message.reply_text('✅ Product data has been refreshed.')
    
    async def transfer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /transfer command"""
        user_id = update.effective_user.id
        
        if not self.permission_service.check_permission(user_id, 'transfer'):
            await update.message.reply_text('⛔ You do not have permission to use this command.')
            return
        
        try:
            # Parse command arguments
            product_imei, from_shop, to_shop = context.args
            from_shop = int(from_shop)
            to_shop = int(to_shop)
            
            success, message = self.transfer_service.transfer_product(
                product_imei, from_shop, to_shop, user_id
            )
            
            if success:
                await update.message.reply_text(f'✅ {message}')
            else:
                await update.message.reply_text(f'❌ {message}')
                
        except ValueError:
            await update.message.reply_text(
                'Usage: /transfer [product_imei] [from_shop_id] [to_shop_id]'
            )
        except Exception as e:
            await update.message.reply_text(f'❌ Error: {str(e)}')
    
    async def update_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /update command"""
        user_id = update.effective_user.id
        
        if not self.permission_service.check_permission(user_id, 'update'):
            await update.message.reply_text('⛔ You do not have permission to use this command.')
            return
        
        try:
            product_id, field, value = context.args
            success = self.product_service.update_product(product_id, field, value)
            
            if success:
                await update.message.reply_text(f'✅ Updated {field} to {value} for product {product_id}')
            else:
                await update.message.reply_text('❌ Update failed. Please check the product ID and field name.')
        except ValueError:
            await update.message.reply_text('Usage: /update [product_id] [field] [value]')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        await self.stats_handler.handle_stats(update, context)
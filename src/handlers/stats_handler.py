from telegram import Update
from telegram.ext import ContextTypes
from services.analytics_service import AnalyticsService
from services.permission_service import PermissionService

class StatsHandler:
    def __init__(self, analytics_service: AnalyticsService, 
                 permission_service: PermissionService):
        self.analytics = analytics_service
        self.permissions = permission_service
    
    async def handle_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        if not self.permissions.check_permission(user_id, 'view_stats'):
            await update.message.reply_text('⛔ You do not have permission to view statistics.')
            return
        
        # Get various statistics
        inventory = self.analytics.get_inventory_summary()
        prices = self.analytics.get_price_analytics()
        shop_stats = self.analytics.get_shop_statistics()
        
        # Format message
        message = [
            "📊 *Inventory Statistics*\n",
            f"Total Products: {inventory['total_products']}",
            f"In Stock: {inventory['in_stock']}",
            f"Out of Stock: {inventory['out_of_stock']}",
            f"Stock Rate: {inventory['stock_rate']}%\n",
            "*Price Analytics*",
            f"Average Price: ${prices['average_price']:,.2f}",
            f"Median Price: ${prices['median_price']:,.2f}",
            f"Price Range: ${prices['min_price']:,.2f} - ${prices['max_price']:,.2f}\n",
            "*Shop Statistics*"
        ]
        
        for shop in shop_stats:
            message.append(
                f"Shop {shop['shop_id']}: {shop['in_stock']}/{shop['total_products']} "
                f"in stock ({shop['models']} models)"
            )
        
        await update.message.reply_text('\n'.join(message), parse_mode='Markdown')
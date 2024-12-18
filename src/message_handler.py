from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import List
from .data_manager import DataManager
from .models import Product
from .exceptions import ProductNotFoundError, InvalidUpdateError
from .utils.formatters import format_search_results
from .utils.analytics import InventoryAnalytics
from config import ADMIN_IDS

class MessageHandler:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.analytics = InventoryAnalytics()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("Search Products", callback_data='search'),
                InlineKeyboardButton("View Stats", callback_data='stats')
            ],
            [InlineKeyboardButton("Help", callback_data='help')]
        ]
        
        if update.effective_user.id in ADMIN_IDS:
            keyboard.append([InlineKeyboardButton("Admin Panel", callback_data='admin')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = (
            "🤖 Welcome to the Mobile Stock Bot! 📱\n\n"
            "Choose an option below or simply send a search term to get started!"
        )
        
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "📱 *Available Commands*\n\n"
            "*Search:*\n"
            "Simply type any of these:\n"
            "- Model name (e.g., 'iPhone 13')\n"
            "- RAM size (e.g., '6GB')\n"
            "- Network type (e.g., '5G')\n\n"
            "*General Commands:*\n"
            "/start - Show main menu\n"
            "/help - Show this help message\n"
            "/stats - Show inventory statistics\n\n"
            "*Admin Commands:*\n"
            "/update model field value - Update product details\n"
            "/refresh - Reload data from Excel\n"
            "/analytics - Detailed inventory analytics"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def analytics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin access required")
            return
        
        products = self.data_manager.search_products("")
        
        # Get analytics
        stock_summary = self.analytics.get_stock_summary(products)
        price_analytics = self.analytics.get_price_analytics(products)
        model_dist = self.analytics.get_model_distribution(products)
        
        # Format message
        analytics_msg = (
            "📊 *Detailed Inventory Analytics*\n\n"
            "*Stock Summary:*\n"
            f"Total Products: {stock_summary['total']}\n"
            f"In Stock: {stock_summary['in_stock']}\n"
            f"Out of Stock: {stock_summary['out_of_stock']}\n"
            f"Low Stock (≤5): {stock_summary['low_stock']}\n"
            f"Stock Rate: {stock_summary['stock_rate']:.1f}%\n\n"
            "*Price Analytics:*\n"
            f"Average Price: ${price_analytics['avg_price']:,.2f}\n"
            f"Min Price: ${price_analytics['min_price']:,.2f}\n"
            f"Max Price: ${price_analytics['max_price']:,.2f}\n\n"
            "*Model Distribution:*\n"
        )
        
        # Add model distribution
        for model, count in model_dist.items():
            analytics_msg += f"{model}: {count} variants\n"
        
        await update.message.reply_text(analytics_msg, parse_mode='Markdown')

    # ... (rest of the existing methods remain the same)
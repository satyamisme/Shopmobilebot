from telegram import Update
from telegram.ext import ContextTypes
from ..utils.data_manager import DataManager
from ..utils.message_formatter import MessageFormatter
from ..utils.exceptions import DataError, ProductNotFoundError
from ..utils.logger import setup_logger

logger = setup_logger()

class MessageHandler:
    def __init__(self):
        try:
            self.data_manager = DataManager()
            self.formatter = MessageFormatter()
            logger.info("MessageHandler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MessageHandler: {str(e)}")
            raise

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            welcome_msg = (
                "👋 Welcome to Mobile Inventory Bot!\n\n"
                "You can search products by sending any of these:\n"
                "- Model name (e.g., 'iPhone 13')\n"
                "- RAM (e.g., '8GB')\n"
                "- Storage (e.g., '256GB')\n"
                "- Network (e.g., '5G')\n"
                "- Color (e.g., 'Blue')\n\n"
                "Commands:\n"
                "/start - Show this message\n"
                "/help - Show help message\n"
                "/stock - Check low stock products"
            )
            await update.message.reply_text(welcome_msg)
            logger.info(f"Start command handled for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in start command: {str(e)}")
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        try:
            help_msg = (
                "*Search Examples:*\n"
                "• iPhone 13\n"
                "• 8GB RAM\n"
                "• 256GB\n"
                "• 5G\n"
                "• Blue\n\n"
                "*Available Commands:*\n"
                "/start - Start the bot\n"
                "/help - Show this help\n"
                "/stock - Check low stock products"
            )
            await update.message.reply_text(help_msg, parse_mode='Markdown')
            logger.info(f"Help command handled for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in help command: {str(e)}")
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")

    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle search queries"""
        try:
            query = update.message.text.strip()
            products = self.data_manager.search_products(query)
            
            await update.message.reply_text(
                self.formatter.format_search_results(products, query),
                parse_mode='Markdown'
            )

            for product in products[:5]:
                await update.message.reply_text(
                    self.formatter.format_product(product),
                    parse_mode='Markdown'
                )
            
            if len(products) > 5:
                await update.message.reply_text(
                    f"Showing top 5 results out of {len(products)} matches."
                )
            
            logger.info(f"Search handled for user {update.effective_user.id}, query: '{query}'")
        except DataError as e:
            logger.warning(f"Search error for user {update.effective_user.id}: {str(e)}")
            await update.message.reply_text(f"Search error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in search: {str(e)}")
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")

    async def stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stock command"""
        try:
            low_stock = self.data_manager.get_low_stock_products()
            
            if not low_stock:
                await update.message.reply_text("No products with low stock.")
                return

            await update.message.reply_text(
                f"📉 Found {len(low_stock)} products with low stock:"
            )

            for product in low_stock:
                await update.message.reply_text(
                    self.formatter.format_product(product),
                    parse_mode='Markdown'
                )
            
            logger.info(f"Stock command handled for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in stock command: {str(e)}")
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")
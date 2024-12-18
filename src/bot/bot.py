from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .handlers import MessageHandler as BotMessageHandler
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.handler = BotMessageHandler()

    async def start(self):
        """Initialize and start the bot"""
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.handler.start))
        app.add_handler(CommandHandler("help", self.handler.help))
        app.add_handler(CommandHandler("stock", self.handler.stock))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.search))
        
        # Start bot
        await app.initialize()
        await app.start()
        await app.run_polling()

def run_bot():
    """Run the Telegram bot"""
    bot = TelegramBot()
    import asyncio
    asyncio.run(bot.start())
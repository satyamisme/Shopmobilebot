from telegram.ext import Application, CommandHandler, MessageHandler, filters
from loguru import logger
from database.database import Database
from services.data_sync import DataSyncService
from handlers.command_handler import CommandHandler
from handlers.message_handler import MessageHandler
import os
from dotenv import load_dotenv

load_dotenv()

async def start():
    """Initialize and start the bot"""
    # Initialize database
    db = Database()
    await db.init_db()
    session = await db.get_session()
    
    # Initialize services
    data_sync = DataSyncService(session)
    await data_sync.sync_from_excel()
    
    # Initialize bot
    app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Initialize handlers
    command_handler = CommandHandler(session)
    message_handler = MessageHandler(session)
    
    # Add handlers
    app.add_handler(CommandHandler('start', command_handler.start))
    app.add_handler(CommandHandler('help', command_handler.help))
    app.add_handler(CommandHandler('refresh', command_handler.refresh))
    app.add_handler(CommandHandler('stats', command_handler.stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_message))
    
    # Start bot
    logger.info("Starting bot...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(start())
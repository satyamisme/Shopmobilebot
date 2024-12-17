import asyncio
from multiprocessing import Process
from src.bot.bot import run_bot
from src.web.main import run_web
from src.database.init_db import init_db
import os

def main():
    # Initialize database if it doesn't exist
    if not os.path.exists('data/inventory.db'):
        init_db()
    
    # Start web interface in a separate process
    web_process = Process(target=run_web)
    web_process.start()
    
    # Run bot in main process
    run_bot()

if __name__ == "__main__":
    main()
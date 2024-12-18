from src.bot.bot import run_bot
from src.utils.excel_generator import MobileDataGenerator
import os

def main():
    # Generate sample data if it doesn't exist
    if not os.path.exists('data/products.xlsx'):
        generator = MobileDataGenerator()
        generator.save_excel()
    
    # Run the bot
    run_bot()

if __name__ == "__main__":
    main()
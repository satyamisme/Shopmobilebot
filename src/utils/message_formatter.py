from typing import Dict, List

class MessageFormatter:
    @staticmethod
    def format_product(product: Dict) -> str:
        """Format a single product for Telegram message"""
        return (
            f"📱 *{product['Brand']} {product['Model']}*\n"
            f"💾 RAM: {product['RAM']}\n"
            f"💽 Storage: {product['Storage']}\n"
            f"📡 Network: {product['Network']}\n"
            f"📸 Camera: {product['Camera']}\n"
            f"🎨 Color: {product['Color']}\n"
            f"📦 Stock: {product['Stock']}\n"
            f"💰 Price: ${product['Price']:,.2f}\n"
            f"📊 Condition: {product['Condition']}"
        )

    @staticmethod
    def format_search_results(products: List[Dict], query: str) -> str:
        """Format search results"""
        if not products:
            return f"No products found matching '{query}'"
        
        return f"Found {len(products)} products matching '{query}':"
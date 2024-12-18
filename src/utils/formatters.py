def format_product_details(product: dict) -> str:
    """Format product details for display"""
    details = [
        f"📱 *Model:* {product.get('Model', 'N/A')}",
        f"💾 *RAM:* {product.get('RAM', 'N/A')}",
        f"📡 *Network:* {product.get('Network', 'N/A')}",
        f"💰 *Price:* ${product.get('Price', 0):,.2f}",
        f"📦 *Status:* {product.get('Status', 'N/A')}"
    ]
    
    if product.get('IMEI'):
        details.append(f"🔢 *IMEI:* {product['IMEI']}")
    
    return '\n'.join(details)

def format_help_message(role: str) -> str:
    """Format help message based on user role"""
    base_commands = [
        "🔍 *Search Commands:*",
        "- Send any text to search products",
        "- Format: `ram:4gb` or just `4gb`",
        "- Format: `network:5g` or just `5g`",
        "- Format: `model:iphone`",
        "\n📱 *Examples:*",
        "- `4gb` (search by RAM)",
        "- `5g` (search by network)",
        "- `iphone 13` (search by model)",
    ]
    
    role_commands = {
        'admin': [
            "\n⚡ *Admin Commands:*",
            "/refresh - Reload product data",
            "/update - Update product details",
            "/transfer - Transfer products",
            "/stats - View statistics"
        ],
        'power_user': [
            "\n🔧 *Power User Commands:*",
            "/refresh - Reload product data",
            "/transfer - Transfer products"
        ],
        'user': []
    }
    
    return '\n'.join(base_commands + role_commands.get(role, []))
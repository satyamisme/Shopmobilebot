# Inventory Management System with Telegram Bot

A comprehensive inventory management system with a Telegram bot interface and web dashboard.

## Features

- 🤖 Telegram Bot Interface
- 🌐 Web Dashboard
- 📊 Excel Data Sync
- 👥 Role-based Access Control
- 🔒 Secure Authentication
- 📱 Product Search and Management

## Prerequisites

- Python 3.11+
- PostgreSQL (optional, SQLite by default)
- Telegram Bot Token (from @BotFather)

## Configuration

1. Create a `.env` file with the following variables:

```env
# Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Database
DATABASE_URL=sqlite+aiosqlite:///data/inventory.db

# Web Interface
SECRET_KEY=your_secret_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# User Management
ADMIN_IDS=123456789,987654321
POWER_USER_IDS=111222333,444555666

# Permissions
ADMIN_PERMISSIONS=all
POWER_USER_PERMISSIONS=search,refresh,transfer,view_stats
USER_PERMISSIONS=search

# Excel Configuration
EXCEL_FILE_PATH=data/products.xlsx
```

## Direct VPS Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/inventory-bot.git
cd inventory-bot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python -m alembic upgrade head
```

5. Place your Excel file in `data/products.xlsx`

6. Start the application:
```bash
python src/run.py
```

## Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/inventory-bot.git
cd inventory-bot
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

## Usage

### Telegram Bot Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/refresh` - Refresh product data (admin only)

### Search Examples

- Model search: `iPhone 13`
- RAM search: `6GB`
- Network search: `5G`
- Storage search: `128GB`

### Web Dashboard

Access the web dashboard at `http://your-server:8000`

Default credentials:
- Username: admin
- Password: (from .env file)

## Directory Structure

```
.
├── data/                  # Data directory for Excel files and SQLite DB
├── src/                   # Source code
│   ├── bot/              # Telegram bot code
│   ├── database/         # Database models and configuration
│   ├── services/         # Business logic services
│   ├── web/              # Web interface
│   └── utils/            # Utility functions
├── logs/                 # Log files
├── tests/                # Test files
├── .env                  # Environment variables
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

## Maintenance

### Logs

- Telegram Bot: `logs/telegram_bot.out.log`
- Web Interface: `logs/web_interface.out.log`
- Supervisor: `logs/supervisord.log`

### Backup

1. Database backup:
```bash
sqlite3 data/inventory.db ".backup 'backup.db'"
```

2. Excel backup:
```bash
cp data/products.xlsx data/products_backup_$(date +%Y%m%d).xlsx
```

## Security Considerations

1. Always use strong passwords
2. Keep the `.env` file secure
3. Regularly update dependencies
4. Monitor log files for suspicious activities
5. Use HTTPS for production web interface

## Troubleshooting

1. If the bot doesn't respond:
   - Check `logs/telegram_bot.err.log`
   - Verify TELEGRAM_BOT_TOKEN
   - Ensure internet connectivity

2. If web interface is inaccessible:
   - Check `logs/web_interface.err.log`
   - Verify port 8000 is open
   - Check server firewall settings

3. Database issues:
   - Check file permissions
   - Verify DATABASE_URL
   - Check disk space

## Support

For issues and feature requests, please create an issue in the repository.
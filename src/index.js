import { config } from 'dotenv';
import { setupBot } from './bot/bot.js';
import { DatabaseService } from './services/database.service.js';
import { logger } from './utils/logger.js';
import { DataSyncService } from './services/dataSync.service.js';

// Load environment variables
config();

async function startBot() {
  try {
    // Initialize services
    const db = new DatabaseService();
    await db.initialize();
    
    const dataSync = new DataSyncService(db);
    await dataSync.syncFromExcel();
    
    // Start the bot
    const bot = setupBot(db, dataSync);
    
    // Set up periodic sync if enabled
    if (process.env.AUTO_SYNC_INTERVAL) {
      const interval = parseInt(process.env.AUTO_SYNC_INTERVAL) * 60 * 1000;
      setInterval(() => dataSync.syncFromExcel(), interval);
    }
    
    logger.info('Bot started successfully');
  } catch (error) {
    logger.error('Failed to start bot:', error);
    process.exit(1);
  }
}

startBot();
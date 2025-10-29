import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

from config import Config
from models import Session, BotConfig, ScheduledMessage, EmergencyMessage
from database import db
from scheduler import MessageScheduler
from utils import validate_time, parse_message_text, setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class TelegramScheduledBot:
    """Main Telegram bot class."""
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        self.application = Application.builder().token(self.config.BOT_TOKEN).build()
        self.scheduler = MessageScheduler(self.application)
        
        self.setup_handlers()
        self.load_existing_schedules()
    
    def setup_handlers(self):
        """Setup all Telegram handlers."""
        handlers = [
            CommandHandler("start", self.start),
            CommandHandler("help", self.help_command),
            CommandHandler("channel", self.set_channel),
            CommandHandler("schedule", self.schedule_message),
            CommandHandler("listschedule", self.list_schedules),
            CommandHandler("removeschedule", self.remove_schedule),
            CommandHandler("info", self.bot_info),
            CommandHandler("epo", self.emergency_message),
            CommandHandler("backup", self.backup_database),
            CallbackQueryHandler(self.button_handler),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message),
        ]
        
        for handler in handlers:
            self.application.add_handler(handler)
    
    def load_existing_schedules(self):
        """Load existing schedules from database."""
        with db.get_session() as session:
            active_messages = session.query(ScheduledMessage).filter_by(is_active=True).all()
            
            channel_config = session.query(BotConfig).filter_by(is_active=True).first()
            if not channel_config:
                logger.warning("No channel configured")
                return
            
            for msg in active_messages:
                self.scheduler.schedule_message(
                    msg.id, msg.scheduled_time, channel_config.channel_id, msg.message_text
                )
            
            logger.info(f"Loaded {len(active_messages)} scheduled messages")
    
    # ... (Include all the bot methods from previous implementation)
    # start, set_channel, schedule_message, handle_message, etc.
    # These would be the same as in the previous bot implementation
    
    async def emergency_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send emergency message immediately."""
        user_id = update.effective_user.id
        
        if not await self.is_user_admin(user_id):
            await update.message.reply_text("❌ Admin access required.")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /epo <message>")
            return
        
        message_text = ' '.join(context.args)
        channel_config = self.get_channel_config()
        
        if not channel_config:
            await update.message.reply_text("❌ No channel configured!")
            return
        
        try:
            # Send immediately
            await self.application.bot.send_message(
                chat_id=channel_config.channel_id,
                text=f"🚨 EMERGENCY MESSAGE:\n\n{message_text}"
            )
            
            # Log to database
            with db.get_session() as session:
                emergency_msg = EmergencyMessage(
                    message_text=message_text,
                    sent_by=user_id,
                    is_sent=True
                )
                session.add(emergency_msg)
            
            await update.message.reply_text("✅ Emergency message sent!")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to send emergency message: {e}")
    
    async def backup_database(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Backup database command."""
        user_id = update.effective_user.id
        
        if not await self.is_user_admin(user_id):
            await update.message.reply_text("❌ Admin access required.")
            return
        
        try:
            backup_path = db.backup_database()
            if backup_path:
                await update.message.reply_document(
                    document=open(backup_path, 'rb'),
                    filename='bot_backup.db',
                    caption="📦 Database backup"
                )
            else:
                await update.message.reply_text("❌ Backup not supported for current database type.")
        except Exception as e:
            await update.message.reply_text(f"❌ Backup failed: {e}")
    
    def run(self):
        """Run the bot."""
        logger.info("Starting Telegram Scheduled Message Bot...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramScheduledBot()
    bot.run()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import Config
import logging

logger = logging.getLogger(__name__)

class MessageScheduler:
    """Message scheduling management."""
    
    def __init__(self, bot_application):
        self.bot_app = bot_application
        self.scheduler = BackgroundScheduler()
        self.setup_scheduler()
    
    def setup_scheduler(self):
        """Setup the scheduler with job stores."""
        jobstores = {
            'default': SQLAlchemyJobStore(url=Config.DATABASE_URL.replace('sqlite:///', 'sqlite:///'))
        }
        
        self.scheduler = BackgroundScheduler(jobstores=jobstores)
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def schedule_message(self, message_id: int, time_str: str, chat_id: str, message_text: str):
        """Schedule a message."""
        hour, minute = time_str.split(':')
        
        trigger = CronTrigger(hour=int(hour), minute=int(minute))
        
        self.scheduler.add_job(
            self.send_scheduled_message,
            trigger=trigger,
            id=str(message_id),
            args=[chat_id, message_text],
            replace_existing=True,
            name=f"Scheduled message {message_id}"
        )
        
        logger.info(f"Scheduled message {message_id} for {time_str}")
    
    def remove_schedule(self, message_id: int):
        """Remove a scheduled message."""
        try:
            self.scheduler.remove_job(str(message_id))
            logger.info(f"Removed schedule {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing schedule {message_id}: {e}")
            return False
    
    async def send_scheduled_message(self, chat_id: str, message_text: str):
        """Send a scheduled message."""
        try:
            await self.bot_app.bot.send_message(
                chat_id=chat_id,
                text=message_text
            )
            logger.info(f"Sent scheduled message to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send scheduled message to {chat_id}: {e}")
    
    def get_scheduled_jobs(self):
        """Get all scheduled jobs."""
        return self.scheduler.get_jobs()
    
    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler shut down")

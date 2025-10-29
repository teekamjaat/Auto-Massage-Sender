import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the bot."""
    
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_USER_IDS = [int(x.strip()) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x.strip()]
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///schedules.db')
    
    # Scheduler
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in environment variables")
        if not cls.ADMIN_USER_IDS:
            raise ValueError("ADMIN_USER_IDS is required in environment variables")

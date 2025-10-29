import re
import logging
from datetime import datetime
from typing import Optional, Tuple

def validate_time(time_str: str) -> bool:
    """Validate time format HH:MM."""
    try:
        hour, minute = map(int, time_str.split(':'))
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except ValueError:
        return False

def parse_message_text(text: str) -> Optional[Tuple[str, str]]:
    """Parse message text for quick scheduling format (HH:MM message)."""
    time_pattern = r'^(\d{1,2}:\d{2})\s+(.+)$'
    match = re.match(time_pattern, text)
    if match:
        time_str, message = match.groups()
        if validate_time(time_str):
            return time_str, message
    return None

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

def format_time_remaining(target_time: str) -> str:
    """Format time remaining until scheduled message."""
    now = datetime.now()
    target = datetime.strptime(target_time, '%H:%M').replace(
        year=now.year, month=now.month, day=now.day
    )
    
    if target < now:
        target = target.replace(day=now.day + 1)
    
    time_diff = target - now
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    return f"{hours}h {minutes}m"

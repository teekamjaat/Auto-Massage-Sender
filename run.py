#!/usr/bin/env python3
"""
Main entry point for the Telegram Scheduled Message Bot.
"""

import signal
import sys
import logging
from bot import TelegramScheduledBot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def signal_handler(sig, frame):
    """Handle shutdown signals."""
    print('\n🛑 Shutting down bot...')
    sys.exit(0)

def main():
    """Main function."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("🚀 Starting Telegram Scheduled Message Bot...")
        bot = TelegramScheduledBot()
        bot.run()
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

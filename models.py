from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config

Base = declarative_base()

class BotConfig(Base):
    __tablename__ = 'bot_config'
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(100))
    channel_title = Column(String(255))
    set_by = Column(Integer)
    set_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class ScheduledMessage(Base):
    __tablename__ = 'scheduled_messages'
    
    id = Column(Integer, primary_key=True)
    message_text = Column(Text, nullable=False)
    scheduled_time = Column(String(5), nullable=False)  # HH:MM
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    message_type = Column(String(20), default='text')

class EmergencyMessage(Base):
    __tablename__ = 'emergency_messages'
    
    id = Column(Integer, primary_key=True)
    message_text = Column(Text, nullable=False)
    sent_by = Column(Integer, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)

# Database setup
engine = create_engine(Config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

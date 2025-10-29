from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import Config

class DatabaseManager:
    """Database management class."""
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    @contextmanager
    def get_session(self):
        """Get database session with context manager."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Create all tables."""
        from models import Base
        Base.metadata.create_all(self.engine)
    
    def backup_database(self, backup_path='backup.db'):
        """Create a backup of the database."""
        import shutil
        import sqlite3
        
        if Config.DATABASE_URL.startswith('sqlite'):
            original_db = Config.DATABASE_URL.replace('sqlite:///', '')
            shutil.copy2(original_db, backup_path)
            return backup_path
        return None

# Global database instance
db = DatabaseManager()

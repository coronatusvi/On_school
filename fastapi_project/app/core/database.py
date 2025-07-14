from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings


class DatabaseManager:
    """
    Lớp quản lý database sử dụng OOP principles
    Singleton pattern để đảm bảo chỉ có một kết nối database
    """
    
    _instance = None
    _engine = None
    _session_local = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._init_database()
    
    def _init_database(self):
        """Khởi tạo engine và session factory"""
        try:
            self._engine = create_engine(
                settings.database_url,
                connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
            )
            self._session_local = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
            print(f"✅ Database engine initialized: {settings.database_url}")
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            raise RuntimeError(f"Database initialization failed: {e}")
    
    @property
    def engine(self):
        """Property để truy cập engine"""
        if self._engine is None:
            raise RuntimeError("Database engine not initialized")
        return self._engine
    
    def get_session(self) -> Generator[Session, None, None]:
        """Generator để tạo database session"""
        if self._session_local is None:
            raise RuntimeError("Database session factory not initialized")
        
        db = self._session_local()
        try:
            yield db
        except Exception as e:
            print(f"❌ Database session error: {e}")
            db.rollback()
            raise
        finally:
            try:
                db.close()
            except Exception as e:
                print(f"⚠️  Error closing database session: {e}")
    
    def create_tables(self):
        """Tạo tất cả các bảng trong database"""
        try:
            # Import models để đảm bảo metadata được load
            from ..models import user, product
            Base.metadata.create_all(bind=self._engine)
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            raise RuntimeError(f"Table creation failed: {e}")


# Base class cho tất cả models
Base = declarative_base()

# Singleton instance
db_manager = DatabaseManager()

# Dependency function cho FastAPI
def get_database() -> Generator[Session, None, None]:
    """
    Dependency function để inject database session vào routes
    """
    yield from db_manager.get_session()

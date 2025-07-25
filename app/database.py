from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Kết nối đến SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///results.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để kế thừa tạo bảng ORM
Base = declarative_base()

from sqlalchemy.orm import Session
from fastapi import Depends

# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
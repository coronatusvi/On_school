from sqlalchemy import Column, String, Text, Float, DateTime
from datetime import datetime
from .database import Base
from sqlalchemy.orm import Session

class Task(Base):
    __tablename__ = "tasks"

    session = Column(String, primary_key=True, index=True)
    type = Column(String)
    status = Column(String)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)

def save_task(db: Session, session_id: str, option: str):
    db_task = Task(session=session_id, type=option, status="pending", result="")
    db.merge(db_task)  # Thay cho insert or update
    db.commit()

def update_result(db: Session, session_id: str, result: str, duration: float = None):
    task = db.query(Task).filter(Task.session == session_id).first()
    if task:
        task.status = "done"
        task.result = result
        if duration:
            task.duration = duration
        db.commit()

def fetch_result(db: Session, session_id: str):
    return db.query(Task).filter(Task.session == session_id).first()
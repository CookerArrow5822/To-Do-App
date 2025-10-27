from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from db import Base, engine


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due = Column(DateTime, nullable=True) # scheduled time (start)
    duration_min = Column(Integer, nullable=True) # duration estimate
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)
from sqlalchemy import Column, Integer, String, Text, Boolean
from src.utils.db import Base

class TaskModel(Base):
    
    __tablename__ = "user_tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
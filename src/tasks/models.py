from sqlalchemy import Column, Integer, String, Text, Boolean
from src.utils.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class TaskModel(Base):
    
    __tablename__ = "user_tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
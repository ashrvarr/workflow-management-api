from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))

    title = Column(String)
    description = Column(String)

    status = Column(String, default="todo")
    priority = Column(String, default="medium")

    due_date = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
from sqlalchemy.orm import Session
from app.models.task import Task

def create_task(db: Session, data):
    task = Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()

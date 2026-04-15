from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.security import get_db, get_current_user
from app.models.task import Task
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# 1. Tasks per user
@router.get("/tasks-per-user")
def tasks_per_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = db.query(Task.assigned_to, Task.id).all()

    stats = {}

    for task in result:
        user_id = task[0]
        stats[user_id] = stats.get(user_id, 0) + 1

    return stats



@router.get("/completed")
def completed_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Task).filter(Task.status == "done").count()


@router.get("/overdue")
def overdue_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    now = datetime.utcnow()

    return db.query(Task).filter(
        Task.due_date != None,
        Task.due_date < now,
        Task.status != "done"
    ).count()
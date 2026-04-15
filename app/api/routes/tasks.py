from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_db, get_current_user, is_admin
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.user import User


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = Task(
        project_id=data.project_id,
        assigned_to=data.assigned_to,
        title=data.title,
        description=data.description,
        priority=data.priority,
        due_date=data.due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {"message": "Task created", "task_id": task.id}

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Task).all()

@router.get("/")
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Task).offset(skip).limit(limit).all()



@router.patch("/{task_id}")
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.status:
        task.status = data.status

    if data.priority:
        task.priority = data.priority

    if data.description:
        task.description = data.description

    db.commit()
    db.refresh(task)

    return {"message": "Task updated"}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return {"message": "User deleted"}
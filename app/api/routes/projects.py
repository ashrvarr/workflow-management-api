from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_db, get_current_user
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create_project(
    name: str,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = Project(
        name=name,
        team_id=team_id,
        description="Created via API"
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created",
        "project_id": project.id
    }
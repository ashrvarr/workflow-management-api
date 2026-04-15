from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_db
from app.models.team import Team
from app.models.membership import Membership
from app.schemas.team import TeamCreate
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/")
def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = Team(name=data.name)
    db.add(team)
    db.commit()
    db.refresh(team)

    # auto add creator as owner
    membership = Membership(
        user_id=current_user.id,
        team_id=team.id,
        role="owner"
    )

    db.add(membership)
    db.commit()

    return {"message": "Team created", "team_id": team.id}
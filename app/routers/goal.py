from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.goal import GoalType
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate
from app.services.goal_service import GoalService

router = APIRouter()


@router.post("", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)) -> GoalRead:
    return GoalService(db).create_goal(payload)


@router.get("", response_model=list[GoalRead])
def list_goals(goal_type: GoalType | None = None, db: Session = Depends(get_db)) -> list[GoalRead]:
    return GoalService(db).list_goals(goal_type)


@router.get("/{goal_id}", response_model=GoalRead)
def get_goal(goal_id: int, db: Session = Depends(get_db)) -> GoalRead:
    return GoalService(db).get_goal(goal_id)


@router.patch("/{goal_id}", response_model=GoalRead)
def update_goal(goal_id: int, payload: GoalUpdate, db: Session = Depends(get_db)) -> GoalRead:
    return GoalService(db).update_goal(goal_id, payload)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)) -> Response:
    GoalService(db).delete_goal(goal_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

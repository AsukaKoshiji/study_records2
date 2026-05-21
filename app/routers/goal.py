from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.post("")
def create_goal(db: Session = Depends(get_db)):
    pass


@router.get("")
def list_goals(db: Session = Depends(get_db)):
    pass


@router.get("/{goal_id}")
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    pass


@router.patch("/{goal_id}")
def update_goal(goal_id: int, db: Session = Depends(get_db)):
    pass


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    pass
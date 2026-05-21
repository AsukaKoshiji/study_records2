from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("")
def get_calendar(db: Session = Depends(get_db)):
    pass
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.calendar import CalendarDay
from app.services.progress_service import ProgressService

router = APIRouter()


@router.get("", response_model=list[CalendarDay])
def get_calendar(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
) -> list[CalendarDay]:
    return ProgressService(db).calendar(year, month)

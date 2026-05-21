from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.progress import ProgressSummary
from app.services.progress_service import ProgressService

router = APIRouter()


@router.get("", response_model=ProgressSummary)
def get_progress(target_date: date = Query(...), db: Session = Depends(get_db)) -> ProgressSummary:
    return ProgressService(db).summary(target_date)

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.study_record_repository import StudyRecordRepository
from app.schemas.study_record import StudyRecordCreate, StudyRecordRead, StudyRecordUpdate

router = APIRouter()


@router.post("", response_model=StudyRecordRead, status_code=status.HTTP_201_CREATED)
def create_study_record(payload: StudyRecordCreate, db: Session = Depends(get_db)) -> StudyRecordRead:
    return StudyRecordRepository(db).create(payload)


@router.get("", response_model=list[StudyRecordRead])
def list_study_records(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
) -> list[StudyRecordRead]:
    return StudyRecordRepository(db).list(start_date, end_date)


@router.get("/{record_id}", response_model=StudyRecordRead)
def get_study_record(record_id: int, db: Session = Depends(get_db)) -> StudyRecordRead:
    record = StudyRecordRepository(db).get(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学習記録が見つかりません。")
    return record


@router.patch("/{record_id}", response_model=StudyRecordRead)
def update_study_record(
    record_id: int,
    payload: StudyRecordUpdate,
    db: Session = Depends(get_db),
) -> StudyRecordRead:
    repository = StudyRecordRepository(db)
    record = repository.get(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学習記録が見つかりません。")
    return repository.update(record, payload)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study_record(record_id: int, db: Session = Depends(get_db)) -> Response:
    repository = StudyRecordRepository(db)
    record = repository.get(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学習記録が見つかりません。")
    repository.delete(record)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

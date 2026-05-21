from __future__ import annotations

from datetime import date

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.study_record import StudyRecord
from app.schemas.study_record import StudyRecordCreate, StudyRecordUpdate


class StudyRecordRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: StudyRecordCreate) -> StudyRecord:
        record = StudyRecord(**payload.model_dump())
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list(self, start_date: date | None = None, end_date: date | None = None) -> list[StudyRecord]:
        stmt: Select[tuple[StudyRecord]] = select(StudyRecord)
        if start_date:
            stmt = stmt.where(StudyRecord.study_date >= start_date)
        if end_date:
            stmt = stmt.where(StudyRecord.study_date <= end_date)
        stmt = stmt.order_by(StudyRecord.study_date.desc(), StudyRecord.id.desc())
        return list(self.db.scalars(stmt).all())

    def get(self, record_id: int) -> StudyRecord | None:
        return self.db.get(StudyRecord, record_id)

    def update(self, record: StudyRecord, payload: StudyRecordUpdate) -> StudyRecord:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, key, value)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: StudyRecord) -> None:
        self.db.delete(record)
        self.db.commit()

    def total_minutes_between(self, start_date: date, end_date: date) -> int:
        stmt = select(func.coalesce(func.sum(StudyRecord.study_minutes), 0)).where(
            StudyRecord.study_date >= start_date,
            StudyRecord.study_date <= end_date,
        )
        return int(self.db.scalar(stmt) or 0)

    def daily_totals_between(self, start_date: date, end_date: date) -> dict[date, int]:
        stmt = (
            select(StudyRecord.study_date, func.sum(StudyRecord.study_minutes).label("total_minutes"))
            .where(StudyRecord.study_date >= start_date, StudyRecord.study_date <= end_date)
            .group_by(StudyRecord.study_date)
        )
        return {row.study_date: int(row.total_minutes) for row in self.db.execute(stmt).all()}

    def study_dates_until(self, end_date: date) -> list[date]:
        stmt = (
            select(StudyRecord.study_date)
            .where(StudyRecord.study_date <= end_date)
            .group_by(StudyRecord.study_date)
            .order_by(StudyRecord.study_date.desc())
        )
        return list(self.db.scalars(stmt).all())

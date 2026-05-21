from datetime import date

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

    def list(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[StudyRecord]:
        query = self.db.query(StudyRecord)

        if start_date:
            query = query.filter(StudyRecord.study_date >= start_date)

        if end_date:
            query = query.filter(StudyRecord.study_date <= end_date)

        return query.order_by(StudyRecord.study_date.desc()).all()

    def get(self, record_id: int) -> StudyRecord | None:
        return (
            self.db.query(StudyRecord)
            .filter(StudyRecord.id == record_id)
            .first()
        )

    def update(
        self,
        record: StudyRecord,
        payload: StudyRecordUpdate,
    ) -> StudyRecord:
        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(record, key, value)

        self.db.commit()
        self.db.refresh(record)

        return record

    def delete(self, record: StudyRecord) -> None:
        self.db.delete(record)
        self.db.commit()
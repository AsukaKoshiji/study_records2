from datetime import date, datetime

from pydantic import BaseModel, Field


class StudyRecordBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=100)
    study_date: date
    duration_minutes: int = Field(..., gt=0)
    memo: str | None = Field(default=None, max_length=1000)


class StudyRecordCreate(StudyRecordBase):
    pass


class StudyRecordUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    subject: str | None = Field(default=None, min_length=1, max_length=100)
    study_date: date | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    memo: str | None = Field(default=None, max_length=1000)


class StudyRecordRead(StudyRecordBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class StudyRecordBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    study_minutes: int = Field(..., gt=0, description="学習時間（分）")
    study_date: date
    memo: str | None = None


class StudyRecordCreate(StudyRecordBase):
    pass


class StudyRecordUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)
    study_minutes: int | None = Field(default=None, gt=0)
    study_date: date | None = None
    memo: str | None = None


class StudyRecordRead(StudyRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

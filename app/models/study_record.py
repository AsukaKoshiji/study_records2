from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StudyRecord(Base):
    __tablename__ = "study_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    subject: Mapped[str] = mapped_column(String(100), nullable=False)

    study_date: Mapped[date] = mapped_column(Date, nullable=False)

    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    memo: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
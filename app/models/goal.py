from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, Enum, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class GoalType(StrEnum):
    daily = "daily"
    monthly = "monthly"


class Goal(Base):
    __tablename__ = "goals"
    __table_args__ = (UniqueConstraint("goal_type", "target_date", name="uq_goals_goal_type_target_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    goal_type: Mapped[GoalType] = mapped_column(Enum(GoalType), nullable=False, index=True)
    target_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

from datetime import date

from pydantic import BaseModel


class CalendarDay(BaseModel):
    date: date
    study_minutes: int
    target_minutes: int | None
    achievement_rate: float | None
    is_achieved: bool | None

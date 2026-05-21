from datetime import date

from pydantic import BaseModel


class DailyProgress(BaseModel):
    date: date
    study_minutes: int
    target_minutes: int | None
    achievement_rate: float | None
    is_achieved: bool | None


class MonthlyProgress(BaseModel):
    year: int
    month: int
    study_minutes: int
    target_minutes: int | None
    achievement_rate: float | None
    is_achieved: bool | None


class StreakProgress(BaseModel):
    current_streak_days: int
    longest_streak_days: int


class ProgressSummary(BaseModel):
    daily: DailyProgress
    monthly: MonthlyProgress
    streak: StreakProgress

from pydantic import BaseModel


class ProgressResponse(BaseModel):
    total_study_minutes: int
    streak_days: int
    achievement_rate: float
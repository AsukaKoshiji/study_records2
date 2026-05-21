from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.goal import GoalType


class GoalBase(BaseModel):
    goal_type: GoalType
    target_minutes: int = Field(..., gt=0, description="目標時間（分）")
    target_date: date

    @model_validator(mode="after")
    def validate_target_date(self) -> "GoalBase":
        if self.goal_type == GoalType.monthly and self.target_date.day != 1:
            raise ValueError("月次目標のtarget_dateは対象月の1日を指定してください。")
        return self


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    target_minutes: int = Field(..., gt=0, description="目標時間（分）")


class GoalRead(GoalBase):
    id: int
    achieved_minutes: int
    achievement_rate: float
    is_achieved: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

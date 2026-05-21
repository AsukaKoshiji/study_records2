from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.goal import Goal, GoalType
from app.repositories.goal_repository import GoalRepository
from app.repositories.study_record_repository import StudyRecordRepository
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate
from app.services.date_utils import achievement_rate, month_end


class GoalService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.goals = GoalRepository(db)
        self.records = StudyRecordRepository(db)

    def create_goal(self, payload: GoalCreate) -> GoalRead:
        try:
            goal = self.goals.create(payload)
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="同じ目標種別と対象日の目標がすでに存在します。",
            ) from exc
        return self.to_read(goal)

    def list_goals(self, goal_type: GoalType | None = None) -> list[GoalRead]:
        return [self.to_read(goal) for goal in self.goals.list(goal_type)]

    def get_goal(self, goal_id: int) -> GoalRead:
        return self.to_read(self._get_goal_or_404(goal_id))

    def update_goal(self, goal_id: int, payload: GoalUpdate) -> GoalRead:
        goal = self.goals.update(self._get_goal_or_404(goal_id), payload)
        return self.to_read(goal)

    def delete_goal(self, goal_id: int) -> None:
        self.goals.delete(self._get_goal_or_404(goal_id))

    def to_read(self, goal: Goal) -> GoalRead:
        achieved_minutes = self._achieved_minutes(goal.goal_type, goal.target_date)
        rate = achievement_rate(achieved_minutes, goal.target_minutes) or 0
        return GoalRead(
            id=goal.id,
            goal_type=goal.goal_type,
            target_minutes=goal.target_minutes,
            target_date=goal.target_date,
            achieved_minutes=achieved_minutes,
            achievement_rate=rate,
            is_achieved=achieved_minutes >= goal.target_minutes,
            created_at=goal.created_at,
            updated_at=goal.updated_at,
        )

    def _get_goal_or_404(self, goal_id: int) -> Goal:
        goal = self.goals.get(goal_id)
        if not goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="目標が見つかりません。")
        return goal

    def _achieved_minutes(self, goal_type: GoalType, target_date: date) -> int:
        if goal_type == GoalType.daily:
            return self.records.total_minutes_between(target_date, target_date)
        return self.records.total_minutes_between(target_date, month_end(target_date.year, target_date.month))

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.goal import Goal, GoalType
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: GoalCreate) -> Goal:
        goal = Goal(**payload.model_dump())
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def list(self, goal_type: GoalType | None = None) -> list[Goal]:
        stmt = select(Goal)
        if goal_type:
            stmt = stmt.where(Goal.goal_type == goal_type)
        stmt = stmt.order_by(Goal.target_date.desc(), Goal.id.desc())
        return list(self.db.scalars(stmt).all())

    def get(self, goal_id: int) -> Goal | None:
        return self.db.get(Goal, goal_id)

    def find_by_type_and_date(self, goal_type: GoalType, target_date: date) -> Goal | None:
        stmt = select(Goal).where(Goal.goal_type == goal_type, Goal.target_date == target_date)
        return self.db.scalars(stmt).first()

    def update(self, goal: Goal, payload: GoalUpdate) -> Goal:
        goal.target_minutes = payload.target_minutes
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, goal: Goal) -> None:
        self.db.delete(goal)
        self.db.commit()

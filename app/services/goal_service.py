from sqlalchemy.orm import Session


class GoalService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def calculate_achievement_rate(self):
        pass
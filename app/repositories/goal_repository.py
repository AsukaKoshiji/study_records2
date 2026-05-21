from sqlalchemy.orm import Session


class GoalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self):
        pass

    def list(self):
        pass

    def get(self, goal_id: int):
        pass

    def update(self):
        pass

    def delete(self):
        pass
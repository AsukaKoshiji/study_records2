from sqlalchemy.orm import Session


class ProgressService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_total_study_minutes(self):
        pass

    def get_streak_days(self):
        pass

    def get_progress_summary(self):
        pass
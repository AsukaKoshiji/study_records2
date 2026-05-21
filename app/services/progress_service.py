from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.goal import GoalType
from app.repositories.goal_repository import GoalRepository
from app.repositories.study_record_repository import StudyRecordRepository
from app.schemas.calendar import CalendarDay
from app.schemas.progress import DailyProgress, MonthlyProgress, ProgressSummary, StreakProgress
from app.services.date_utils import achievement_rate, month_end, month_start


class ProgressService:
    def __init__(self, db: Session) -> None:
        self.goals = GoalRepository(db)
        self.records = StudyRecordRepository(db)

    def calendar(self, year: int, month: int) -> list[CalendarDay]:
        start = month_start(year, month)
        end = month_end(year, month)
        daily_totals = self.records.daily_totals_between(start, end)

        days: list[CalendarDay] = []
        current = start
        while current <= end:
            study_minutes = daily_totals.get(current, 0)
            goal = self.goals.find_by_type_and_date(GoalType.daily, current)
            target_minutes = goal.target_minutes if goal else None
            rate = achievement_rate(study_minutes, target_minutes)
            days.append(
                CalendarDay(
                    date=current,
                    study_minutes=study_minutes,
                    target_minutes=target_minutes,
                    achievement_rate=rate,
                    is_achieved=study_minutes >= target_minutes if target_minutes else None,
                )
            )
            current += timedelta(days=1)
        return days

    def summary(self, target_date: date) -> ProgressSummary:
        month_first = month_start(target_date.year, target_date.month)
        month_last = month_end(target_date.year, target_date.month)

        daily_minutes = self.records.total_minutes_between(target_date, target_date)
        monthly_minutes = self.records.total_minutes_between(month_first, month_last)

        daily_goal = self.goals.find_by_type_and_date(GoalType.daily, target_date)
        monthly_goal = self.goals.find_by_type_and_date(GoalType.monthly, month_first)

        daily_target = daily_goal.target_minutes if daily_goal else None
        monthly_target = monthly_goal.target_minutes if monthly_goal else None

        return ProgressSummary(
            daily=DailyProgress(
                date=target_date,
                study_minutes=daily_minutes,
                target_minutes=daily_target,
                achievement_rate=achievement_rate(daily_minutes, daily_target),
                is_achieved=daily_minutes >= daily_target if daily_target else None,
            ),
            monthly=MonthlyProgress(
                year=target_date.year,
                month=target_date.month,
                study_minutes=monthly_minutes,
                target_minutes=monthly_target,
                achievement_rate=achievement_rate(monthly_minutes, monthly_target),
                is_achieved=monthly_minutes >= monthly_target if monthly_target else None,
            ),
            streak=self._streak(target_date),
        )

    def _streak(self, target_date: date) -> StreakProgress:
        study_dates = self.records.study_dates_until(target_date)
        study_date_set = set(study_dates)

        current_streak = 0
        cursor = target_date
        while cursor in study_date_set:
            current_streak += 1
            cursor -= timedelta(days=1)

        longest_streak = 0
        running = 0
        previous: date | None = None
        for study_date in sorted(study_date_set):
            if previous and study_date == previous + timedelta(days=1):
                running += 1
            else:
                running = 1
            longest_streak = max(longest_streak, running)
            previous = study_date

        return StreakProgress(current_streak_days=current_streak, longest_streak_days=longest_streak)

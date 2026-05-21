from calendar import monthrange
from datetime import date


def month_start(year: int, month: int) -> date:
    return date(year, month, 1)


def month_end(year: int, month: int) -> date:
    return date(year, month, monthrange(year, month)[1])


def achievement_rate(actual_minutes: int, target_minutes: int | None) -> float | None:
    if not target_minutes:
        return None
    return round(actual_minutes / target_minutes * 100, 2)

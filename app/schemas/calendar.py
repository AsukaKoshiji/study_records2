from pydantic import BaseModel


class CalendarItem(BaseModel):
    pass


class CalendarResponse(BaseModel):
    items: list[CalendarItem]
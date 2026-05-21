from fastapi import APIRouter

from app.routers import calendar, goal, progress, study_record

api_router = APIRouter()


@api_router.get("", tags=["api"])
def api_index() -> dict[str, list[str]]:
    return {
        "resources": [
            "/study-records",
            "/goals",
            "/calendar",
            "/progress",
        ]
    }


api_router.include_router(study_record.router, prefix="/study-records", tags=["study-records"])
api_router.include_router(goal.router, prefix="/goals", tags=["goals"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])

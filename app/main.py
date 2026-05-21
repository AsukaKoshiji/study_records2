from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Learning Record API",
    description="学習記録、目標、カレンダー、進捗確認を管理するMVP APIです。",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

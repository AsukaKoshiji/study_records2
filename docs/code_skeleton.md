# コードスケルトン

学習記録管理APIのMVP実装で使用する基本構成です。

## ディレクトリ構成

```text
app/
  main.py
  api/
    v1/
      router.py
  routers/
    study_record.py
    goal.py
    calendar.py
    progress.py
  schemas/
    study_record.py
    goal.py
    calendar.py
    progress.py
  models/
    study_record.py
    goal.py
  repositories/
    study_record_repository.py
    goal_repository.py
  services/
    goal_service.py
    progress_service.py
    date_utils.py
  db/
    session.py
    base.py
  core/
    config.py
```

## main.py

```python
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learning Record API")
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

## ルータ層

HTTPリクエストを受け取り、スキーマで入力・出力を定義します。DB操作や集計ロジックはRepositoryやServiceへ委譲します。

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("")
def list_items(db: Session = Depends(get_db)):
    pass
```

対象ファイル:

- `app/routers/study_record.py`
- `app/routers/goal.py`
- `app/routers/calendar.py`
- `app/routers/progress.py`

## スキーマ層

Pydanticでリクエスト・レスポンスの型を定義します。

```python
from pydantic import BaseModel, Field


class ExampleCreate(BaseModel):
    name: str = Field(..., min_length=1)


class ExampleRead(ExampleCreate):
    id: int
```

対象ファイル:

- `app/schemas/study_record.py`
- `app/schemas/goal.py`
- `app/schemas/calendar.py`
- `app/schemas/progress.py`

## モデル層

SQLAlchemyでMySQLのテーブル構造を定義します。

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Example(Base):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

対象ファイル:

- `app/models/study_record.py`
- `app/models/goal.py`

## Repository層

DBへのCRUD処理を担当します。SQLインジェクション対策として、SQLAlchemy ORMを使用します。

```python
from sqlalchemy.orm import Session


class ExampleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload):
        pass

    def list(self):
        pass

    def get(self, item_id: int):
        pass

    def update(self, item, payload):
        pass

    def delete(self, item) -> None:
        pass
```

対象ファイル:

- `app/repositories/study_record_repository.py`
- `app/repositories/goal_repository.py`

## Service層

目標達成率、月次集計、カレンダー表示、継続日数などの業務ロジックを担当します。

```python
from sqlalchemy.orm import Session


class ExampleService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def execute(self):
        pass
```

対象ファイル:

- `app/services/goal_service.py`
- `app/services/progress_service.py`
- `app/services/date_utils.py`

## Docker構成

```text
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

`docker compose up --build` でFastAPIとMySQLを起動します。

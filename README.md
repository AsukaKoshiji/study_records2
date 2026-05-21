# Learning Record API

学習記録をカレンダーに記録し、日次・月次目標と進捗を確認する FastAPI + MySQL のMVPです。

## 技術構成

- Backend: FastAPI
- DB: MySQL
- ORM: SQLAlchemy
- Environment: Docker / Docker Compose

## 起動方法

```bash
docker compose up --build
```

起動後、以下にアクセスできます。

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API一覧

### 学習記録

- `POST /api/v1/study-records`
- `GET /api/v1/study-records`
- `GET /api/v1/study-records/{record_id}`
- `PATCH /api/v1/study-records/{record_id}`
- `DELETE /api/v1/study-records/{record_id}`

### 目標

- `POST /api/v1/goals`
- `GET /api/v1/goals`
- `GET /api/v1/goals/{goal_id}`
- `PATCH /api/v1/goals/{goal_id}`
- `DELETE /api/v1/goals/{goal_id}`

### カレンダー

- `GET /api/v1/calendar?year=2026&month=5`

### 進捗

- `GET /api/v1/progress?target_date=2026-05-21`

## リクエスト例

### 学習記録作成

```json
{
  "title": "FastAPI入門",
  "content": "ルーティングと依存性注入を学習",
  "study_minutes": 90,
  "study_date": "2026-05-21",
  "memo": "Swagger UIで動作確認した"
}
```

### 日次目標作成

```json
{
  "goal_type": "daily",
  "target_minutes": 120,
  "target_date": "2026-05-21"
}
```

### 月次目標作成

月次目標の `target_date` は対象月の1日を指定します。

```json
{
  "goal_type": "monthly",
  "target_minutes": 2400,
  "target_date": "2026-05-01"
}
```

## レイヤード構成

```text
app/
  api/          ルーティング
  core/         設定
  db/           DB接続
  models/       SQLAlchemyモデル
  repositories/ DB操作
  schemas/      Pydanticスキーマ
  services/     進捗・目標などの業務ロジック
```

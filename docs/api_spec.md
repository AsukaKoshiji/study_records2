# API仕様書

Base URL: `/api/v1`

## ヘルスチェック

| Method | Path | 説明 |
|---|---|---|
| GET | `/health` | APIの稼働確認 |

## 学習記録API

### 学習記録作成

`POST /study-records`

Request:

```json
{
  "title": "FastAPI入門",
  "content": "ルーティングと依存性注入を学習",
  "study_minutes": 90,
  "study_date": "2026-05-21",
  "memo": "Swagger UIで確認"
}
```

Response: `201 Created`

```json
{
  "id": 1,
  "title": "FastAPI入門",
  "content": "ルーティングと依存性注入を学習",
  "study_minutes": 90,
  "study_date": "2026-05-21",
  "memo": "Swagger UIで確認",
  "created_at": "2026-05-21T10:00:00",
  "updated_at": "2026-05-21T10:00:00"
}
```

### 学習記録一覧

`GET /study-records?start_date=2026-05-01&end_date=2026-05-31`

### 学習記録詳細

`GET /study-records/{record_id}`

### 学習記録更新

`PATCH /study-records/{record_id}`

Request:

```json
{
  "study_minutes": 120,
  "memo": "復習も実施"
}
```

### 学習記録削除

`DELETE /study-records/{record_id}`

Response: `204 No Content`

## 目標API

### 目標作成

`POST /goals`

日次目標:

```json
{
  "goal_type": "daily",
  "target_minutes": 120,
  "target_date": "2026-05-21"
}
```

月次目標:

```json
{
  "goal_type": "monthly",
  "target_minutes": 2400,
  "target_date": "2026-05-01"
}
```

月次目標の `target_date` は対象月の1日を指定します。

### 目標一覧

`GET /goals`

`GET /goals?goal_type=daily`

### 目標詳細

`GET /goals/{goal_id}`

### 目標更新

`PATCH /goals/{goal_id}`

```json
{
  "target_minutes": 150
}
```

### 目標削除

`DELETE /goals/{goal_id}`

## カレンダーAPI

`GET /calendar?year=2026&month=5`

Response:

```json
[
  {
    "date": "2026-05-21",
    "study_minutes": 90,
    "target_minutes": 120,
    "achievement_rate": 75.0,
    "is_achieved": false
  }
]
```

## 進捗API

`GET /progress?target_date=2026-05-21`

Response:

```json
{
  "daily": {
    "date": "2026-05-21",
    "study_minutes": 90,
    "target_minutes": 120,
    "achievement_rate": 75.0,
    "is_achieved": false
  },
  "monthly": {
    "year": 2026,
    "month": 5,
    "study_minutes": 900,
    "target_minutes": 2400,
    "achievement_rate": 37.5,
    "is_achieved": false
  },
  "streak": {
    "current_streak_days": 3,
    "longest_streak_days": 8
  }
}
```

## エラーレスポンス

| Status | 用途 |
|---|---|
| 404 | 対象データが存在しない |
| 409 | 一意制約に違反する目標を作成した |
| 422 | リクエストバリデーションエラー |

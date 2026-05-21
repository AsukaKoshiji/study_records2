from fastapi.testclient import TestClient


def test_goal_calendar_and_progress(client: TestClient) -> None:
    daily_goal_response = client.post(
        "/api/v1/goals",
        json={
            "goal_type": "daily",
            "target_minutes": 120,
            "target_date": "2026-05-21",
        },
    )
    assert daily_goal_response.status_code == 201

    monthly_goal_response = client.post(
        "/api/v1/goals",
        json={
            "goal_type": "monthly",
            "target_minutes": 2400,
            "target_date": "2026-05-01",
        },
    )
    assert monthly_goal_response.status_code == 201

    client.post(
        "/api/v1/study-records",
        json={
            "title": "FastAPI",
            "content": "CRUD実装",
            "study_minutes": 90,
            "study_date": "2026-05-21",
            "memo": None,
        },
    )
    client.post(
        "/api/v1/study-records",
        json={
            "title": "MySQL",
            "content": "インデックス確認",
            "study_minutes": 60,
            "study_date": "2026-05-22",
            "memo": None,
        },
    )

    goals_response = client.get("/api/v1/goals")
    assert goals_response.status_code == 200
    assert len(goals_response.json()) == 2

    calendar_response = client.get("/api/v1/calendar", params={"year": 2026, "month": 5})
    assert calendar_response.status_code == 200
    calendar_days = calendar_response.json()
    target_day = next(day for day in calendar_days if day["date"] == "2026-05-21")
    assert target_day["study_minutes"] == 90
    assert target_day["target_minutes"] == 120
    assert target_day["achievement_rate"] == 75.0
    assert target_day["is_achieved"] is False

    progress_response = client.get("/api/v1/progress", params={"target_date": "2026-05-21"})
    assert progress_response.status_code == 200
    progress = progress_response.json()
    assert progress["daily"]["study_minutes"] == 90
    assert progress["daily"]["achievement_rate"] == 75.0
    assert progress["monthly"]["study_minutes"] == 150
    assert progress["monthly"]["achievement_rate"] == 6.25
    assert progress["streak"]["current_streak_days"] == 1
    assert progress["streak"]["longest_streak_days"] == 1


def test_monthly_goal_requires_first_day(client: TestClient) -> None:
    response = client.post(
        "/api/v1/goals",
        json={
            "goal_type": "monthly",
            "target_minutes": 2400,
            "target_date": "2026-05-21",
        },
    )
    assert response.status_code == 422


def test_duplicate_goal_returns_conflict(client: TestClient) -> None:
    payload = {
        "goal_type": "daily",
        "target_minutes": 120,
        "target_date": "2026-05-21",
    }
    assert client.post("/api/v1/goals", json=payload).status_code == 201
    assert client.post("/api/v1/goals", json=payload).status_code == 409

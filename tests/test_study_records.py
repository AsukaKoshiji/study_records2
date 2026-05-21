from fastapi.testclient import TestClient


def test_study_record_crud(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/study-records",
        json={
            "title": "FastAPI入門",
            "content": "ルーティングと依存性注入を学習",
            "study_minutes": 90,
            "study_date": "2026-05-21",
            "memo": "pytestで確認",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["study_minutes"] == 90

    list_response = client.get("/api/v1/study-records")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    detail_response = client.get("/api/v1/study-records/1")
    assert detail_response.status_code == 200
    assert detail_response.json()["title"] == "FastAPI入門"

    update_response = client.patch(
        "/api/v1/study-records/1",
        json={"study_minutes": 120, "memo": "復習も実施"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["study_minutes"] == 120
    assert update_response.json()["memo"] == "復習も実施"

    delete_response = client.delete("/api/v1/study-records/1")
    assert delete_response.status_code == 204

    not_found_response = client.get("/api/v1/study-records/1")
    assert not_found_response.status_code == 404


def test_study_record_list_can_filter_by_date(client: TestClient) -> None:
    client.post(
        "/api/v1/study-records",
        json={
            "title": "Python",
            "content": "基礎文法",
            "study_minutes": 60,
            "study_date": "2026-05-20",
            "memo": None,
        },
    )
    client.post(
        "/api/v1/study-records",
        json={
            "title": "SQL",
            "content": "集計",
            "study_minutes": 45,
            "study_date": "2026-05-21",
            "memo": None,
        },
    )

    response = client.get("/api/v1/study-records", params={"start_date": "2026-05-21"})
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["title"] == "SQL"

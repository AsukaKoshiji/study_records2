from fastapi.testclient import TestClient


def test_root_and_health(client: TestClient) -> None:
    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json()["api_prefix"] == "/api/v1"

    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}


def test_api_index(client: TestClient) -> None:
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert "/study-records" in response.json()["resources"]

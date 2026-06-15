from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

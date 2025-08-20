from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_returns_welcome_message() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Practice API"}


def test_hello_endpoint_returns_hello_world() -> None:
    response = client.post("/hello", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"result": "hello world"}



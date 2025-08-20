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


def test_add_endpoint_returns_sum() -> None:
    response = client.post("/add", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"sum": 5}


def test_dropbox_pdfs_without_token_returns_500() -> None:
    # Ensure env var is not set during this test
    import os

    original = os.environ.pop("DROPBOX_ACCESS_TOKEN", None)
    try:
        response = client.post("/dropbox/pdfs", json={"folder_path": "/some/folder"})
        assert response.status_code == 500
        assert response.json()["detail"] == "DROPBOX_ACCESS_TOKEN not configured"
    finally:
        if original is not None:
            os.environ["DROPBOX_ACCESS_TOKEN"] = original



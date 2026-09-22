from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_and_version() -> None:
    assert client.get("/health").json() == {"status": "healthy"}
    assert client.get("/version").json() == {"version": "0.1.0"}


def test_request_telemetry_and_metrics() -> None:
    response = client.get("/health", headers={"X-Request-ID": "test-request"})

    assert response.headers["X-Request-ID"] == "test-request"
    assert response.status_code == 200
    assert b"clamsentinel_http_requests_total" in client.get("/metrics").content


def test_errors_use_envelope() -> None:
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {"error": {"code": "HTTP_404", "message": "Not Found"}}


def test_jwt_scaffold_issues_bearer_token() -> None:
    response = client.post("/api/v1/auth/token", data={"username": "tester", "password": "ignored"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
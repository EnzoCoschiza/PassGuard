from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "passguard-ci-api"}


def test_analyze_password_contract() -> None:
    response = client.post("/password/analyze", json={"password": "UTN@2026segura"})
    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 70
    assert body["level"] == "medium"
    assert [token["type"] for token in body["tokens"]] == [
        "UPPERCASE_WORD",
        "SYMBOL",
        "NUMBER",
        "LOWERCASE_WORD",
    ]
    assert [warning["code"] for warning in body["warnings"]] == ["YEAR_DETECTED"]


def test_missing_password_returns_422() -> None:
    response = client.post("/password/analyze", json={})
    assert response.status_code == 422


def test_non_string_password_returns_422() -> None:
    response = client.post("/password/analyze", json={"password": 1234})
    assert response.status_code == 422

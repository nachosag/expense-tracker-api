from fastapi.testclient import TestClient
# from sqlmodel import Session


def test_register_user(client: TestClient):
    response = client.post(
        "/", json={"email": "user@example.com", "password": "password", "name": "user"}
    )
    # data = response.json()
    assert response.status_code == 404

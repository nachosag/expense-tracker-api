from fastapi.testclient import TestClient
from fastapi import status

def test_successful_signup(client: TestClient):
    response = client.post(
        "/auth/signup",
        json={
            "email": "john.doe@example.com",
            "password": "easy_password",
            "name": "John Doe",
        },
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] == 1
    assert data["email"] == "john.doe@example.com"
    assert data["name"] == "John Doe"
    assert data["expenses"] == []


def test_incomplete_signup(client: TestClient):
    response = client.post(
        "/auth/signup", json={"email": "john.doe@example.com", "password": "easy_password"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_signup(client: TestClient):
    response = client.post(
        "/auth/signup",
        json={
            "email": "john.doeexample.com",
            "password": "easy_password",
            "name": "John Doe",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_duplicated_signup(client: TestClient):
    client.post(
        "/auth/signup",
        json={
            "email": "john.doe@example.com",
            "password": "easy_password",
            "name": "John Doe",
        },
    )
    response = client.post(
        "/auth/signup",
        json={
            "email": "john.doe@example.com",
            "password": "easy_password",
            "name": "John Doe",
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT

from fastapi.testclient import TestClient
from fastapi import status


def test_successful_signup(client: TestClient):
    user_data = {
        "email": "john.doe@example.com",
        "password": "easy_password",
        "name": "John Doe",
    }
    response = client.post(
        "/auth/signup",
        json=user_data,
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] == 1
    assert data["email"] == "john.doe@example.com"
    assert data["name"] == "John Doe"
    assert data["expenses"] == []


def test_incomplete_signup(client: TestClient):
    user_data = {"email": "john.doe@example.com", "password": "easy_password"}
    response = client.post(
        "/auth/signup",
        json=user_data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_signup(client: TestClient):
    user_data = {
        "email": "john.doeexample.com",
        "password": "easy_password",
        "name": "John Doe",
    }
    response = client.post(
        "/auth/signup",
        json=user_data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_duplicated_signup(client: TestClient):
    user_data = {
        "email": "john.doe@example.com",
        "password": "easy_password",
        "name": "John Doe",
    }
    client.post(
        "/auth/signup",
        json=user_data,
    )
    response = client.post(
        "/auth/signup",
        json=user_data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT

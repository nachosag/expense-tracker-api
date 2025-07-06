from ....auth.auth_service import AuthService
from datetime import timedelta
from fastapi import status
from fastapi.testclient import TestClient


def test_successful_login(client: TestClient):
    user_data = {
        "email": "john.doe@example.com",
        "password": "easy_password",
        "name": "John Doe",
    }
    signup_response = client.post(
        "/auth/signup",
        json=user_data,
    ).json()

    response = client.post(
        "/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["access_token"] == AuthService.create_access_token(
        signup_response["email"], signup_response["id"], timedelta(minutes=30)
    )
    assert data["token_type"] == "bearer"


def test_login_with_nonexistent_user(client: TestClient):
    user_data = {"username": "not.exists@gmail.com", "password": "any_password"}
    response = client.post(
        "/auth/login",
        data=user_data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_empty_password(client: TestClient):
    user_data = {
        "email": "john.doe@example.com",
        "password": "easy_password",
        "name": "John Doe",
    }
    signup_response = client.post(
        "/auth/signup",
        json=user_data,
    ).json()

    response = client.post(
        "/auth/login",
        data={"username": signup_response["email"], "password": ""},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_empty_username(client: TestClient):
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
        "/auth/login",
        data={"username": "", "password": "easy_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_missing_fields(client: TestClient):
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
        "/auth/login",
        data={},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

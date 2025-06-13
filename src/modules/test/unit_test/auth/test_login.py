from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session
from ....auth import auth_service, auth_schemas
from datetime import timedelta


def test_successful_login(session: Session, client: TestClient):
    user = auth_service.signup(
        session,
        auth_schemas.SignupRequest(
            email="john.doe@gmail.com", password="secret_password", name="John Doe"
        ),
    )
    response = client.post(
        "/auth/login",
        data={"username": "john.doe@gmail.com", "password": "secret_password"},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["access_token"] == auth_service.create_access_token(
        user.email, user.id, timedelta(minutes=30)
    )
    assert data["token_type"] == "bearer"


def test_login_with_nonexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "not.exists@gmail.com", "password": "any_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_empty_password(session: Session, client: TestClient):
    auth_service.signup(
        session,
        auth_schemas.SignupRequest(
            email="some.username@gmail.com", password="empty_password", name="Empty Pass"
        ),
    )
    response = client.post(
        "/auth/login",
        data={"username": "some.username@gmail.com", "password": ""},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_empty_username(session: Session, client: TestClient):
    auth_service.signup(
        session,
        auth_schemas.SignupRequest(
            email="empty.username@gmail.com", password="some_password", name="Empty Pass"
        ),
    )
    response = client.post(
        "/auth/login",
        data={"username": "", "password": "some_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_missing_fields(session: Session, client: TestClient):
    auth_service.signup(
        session,
        auth_schemas.SignupRequest(
            email="empty.pass@gmail.com", password="empty_password", name="Empty Fields"
        ),
    )
    response = client.post(
        "/auth/login",
        data={},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

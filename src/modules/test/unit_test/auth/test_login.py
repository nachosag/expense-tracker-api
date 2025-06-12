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


def test_unauthorized_login(session: Session, client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "john.doe@gmail.com", "password": "false_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_incomplete_login(session: Session, client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "john.doe@gmail.com"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session
from .....database import models

from typing import Any

def register_user(session: Session, **kwargs: Any):
    user = models.User(**kwargs)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def test_register_user(client: TestClient):
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


def test_register_incomplete_user(client: TestClient):
    response = client.post(
        "/auth/signup", json={"email": "john.doe@example.com", "password": "easy_password"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_invalid_user(client: TestClient):
    response = client.post(
        "/auth/signup",
        json={
            "email": "john.doeexample.com",
            "password": "easy_password",
            "name": "John Doe",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_duplicated_user(client: TestClient):
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

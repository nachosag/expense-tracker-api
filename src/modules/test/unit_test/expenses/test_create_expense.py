from datetime import date
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from typing import Any


def test_create_expense_success(client: TestClient):
    user_data = {
        "email": "john.doe@example.com",
        "password": "fake_password",
        "name": "John Doe",
    }
    client.post(url="/auth/signup", json=user_data)

    token = client.post(
        url="/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    ).json()

    headers = {"Authorization": f"Bearer {token['access_token']}"}

    expense_data: dict[str, Any] = {
        "category_id": 1,
        "amount": 1,
        "description": "string",
        "spent_at": f"{date.today()}",
    }

    response = client.post(url="/expenses/", json=expense_data, headers=headers)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["created_at"].startswith(date.today().isoformat())
    assert data["updated_at"].startswith(date.today().isoformat())
    assert data["category_id"] == 1
    assert data["amount"] == 1
    assert data["description"] == "string"
    assert data["spent_at"] == str(date.today())


def test_create_expense_invalid_data(session: Session, client: TestClient):
    pass


def test_create_expense_incomplete_data(session: Session, client: TestClient):
    pass


def test_create_expense_unauthenticated(session: Session, client: TestClient):
    pass


def test_create_expense_with_unknown_category():
    pass

from datetime import date
from typing import Any
from fastapi.testclient import TestClient
from fastapi import status


def test_get_expense_by_id_success(client: TestClient):
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

    client.post(url="/expenses/", json=expense_data, headers=headers)

    response = client.get(url="/expenses/1", headers=headers)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["category_id"] == 1
    assert data["amount"] == 1
    assert data["description"] == "string"
    assert data["spent_at"] == f"{date.today()}"
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["created_at"].startswith(date.today().isoformat())
    assert data["updated_at"].startswith(date.today().isoformat())


def test_get_expense_not_found(client: TestClient):
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

    client.post(url="/expenses/", json=expense_data, headers=headers)

    response = client.get(url="/expenses/2", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_expense_unauthorized_access(client: TestClient):
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

    client.post(url="/expenses/", json=expense_data, headers=headers)

    response = client.get(url="/expenses/2")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_expense_of_another_user(client: TestClient):
    # Register and login first user
    first_user = {
        "email": "john.doe@example.com",
        "password": "fake_password",
        "name": "John Doe",
    }
    client.post(url="/auth/signup", json=first_user)
    first_user_token = client.post(
        url="/auth/login",
        data={"username": first_user["email"], "password": first_user["password"]},
    ).json()
    first_user_headers = {"Authorization": f"Bearer {first_user_token['access_token']}"}

    # Register and login second user
    second_user = {
        "email": "ana.addams@example.com",
        "password": "1234",
        "name": "Ana Addams",
    }
    client.post(url="/auth/signup", json=second_user)
    second_user_token = client.post(
        url="/auth/login",
        data={"username": second_user["email"], "password": second_user["password"]},
    ).json()
    second_user_headers = {
        "Authorization": f"Bearer {second_user_token['access_token']}"
    }

    # First user creates an expense
    expense_data: dict[str, Any] = {
        "category_id": 1,
        "amount": 10,
        "description": "Lunch",
        "spent_at": f"{date.today()}",
    }
    client.post(url="/expenses/", json=expense_data, headers=first_user_headers)

    # Second user tries to access first user's expense
    response = client.get(url="/expenses/1", headers=second_user_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

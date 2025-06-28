from datetime import date
from typing import Any
from fastapi.testclient import TestClient
from fastapi import status


def test_update_expense_success(client: TestClient):
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

    expense_data: dict[str, Any] = {
        "category_id": 2,
        "amount": 3,
        "description": "New description",
        "spent_at": f"{date.today()}",
    }

    response = client.patch(url="/expenses/1", json=expense_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == 1
    assert data["category_id"] == 2
    assert data["amount"] == 3
    assert data["description"] == "New description"
    assert data["spent_at"] == str(date.today())


def test_update_expense_not_found(client: TestClient):
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

    expense_data: dict[str, Any] = {
        "category_id": 2,
        "amount": 3,
        "description": "New description",
        "spent_at": f"{date.today()}",
    }

    response = client.patch(url="/expenses/2", json=expense_data, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_expense_unauthorized_access(client: TestClient):
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

    expense_data: dict[str, Any] = {
        "category_id": 2,
        "amount": 3,
        "description": "New description",
        "spent_at": f"{date.today()}",
    }

    response = client.patch(url="/expenses/1", json=expense_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_expense_invalid_data(client: TestClient):
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

    expense_data: dict[str, Any] = {
        "category_id": 2,
        "amount": -1,
        "description": "New description",
        "spent_at": f"{date.today()}",
    }

    response = client.patch(url="/expenses/1", json=expense_data, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_expense_incomplete_data(client: TestClient):
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

    expense_data: dict[str, Any] = {
        "category_id": None,
        "amount": 3,
        "description": "New string",
        "spent_at": None,
    }

    response = client.patch(url="/expenses/1", json=expense_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["category_id"] == 1
    assert data["amount"] == 3
    assert data["description"] == "New string"
    assert data["spent_at"] == str(date.today())
    assert data["updated_at"].startswith(date.today().isoformat())

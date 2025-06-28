from datetime import date
from typing import Any
from fastapi.testclient import TestClient
from fastapi import status


def test_delete_expense_success(client: TestClient):
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

    response = client.delete(url="/expenses/1", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(url="/expense/1", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_expense_not_found(client: TestClient):
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

    response = client.delete(url="/expenses/2", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_expense_unauthorized_access(client: TestClient):
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

    response = client.delete(url="/expenses/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_expense_of_another_user(client: TestClient):
    first_user_data = {
        "email": "john.doe@example.com",
        "password": "fake_password",
        "name": "John Doe",
    }
    client.post(url="/auth/signup", json=first_user_data)

    second_user_data = {
        "email": "ana.ruiz@example.com",
        "password": "safest_password",
        "name": "Ana Ruiz",
    }
    client.post(url="/auth/signup", json=second_user_data)

    first_user_token = client.post(
        url="/auth/login",
        data={
            "username": first_user_data["email"],
            "password": first_user_data["password"],
        },
    ).json()

    second_user_token = client.post(
        url="/auth/login",
        data={
            "username": second_user_data["email"],
            "password": second_user_data["password"],
        },
    ).json()

    first_user_headers = {"Authorization": f"Bearer {first_user_token['access_token']}"}
    second_user_headers = {
        "Authorization": f"Bearer {second_user_token['access_token']}"
    }

    expense_data: dict[str, Any] = {
        "category_id": 1,
        "amount": 1,
        "description": "string",
        "spent_at": f"{date.today()}",
    }

    client.post(url="/expenses/", json=expense_data, headers=first_user_headers)

    expense_data: dict[str, Any] = {
        "category_id": 2,
        "amount": 2,
        "description": "Another string",
        "spent_at": f"{date.today()}",
    }

    client.post(url="/expenses/", json=expense_data, headers=second_user_headers)

    response = client.delete(url="/expenses/2", headers=first_user_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.get(url="/expenses/2", headers=second_user_headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == 2
    assert data["category_id"] == 2
    assert data["amount"] == 2
    assert data["description"] == "Another string"
    assert data["spent_at"] == str(date.today())

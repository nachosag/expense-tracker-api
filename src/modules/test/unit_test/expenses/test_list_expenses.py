from datetime import date
from typing import Any
from fastapi.testclient import TestClient
from fastapi import status


def test_list_expenses_is_empty(client: TestClient):
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

    response = client.get(url="/expenses/", headers=headers)
    data: list[Any] = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_expenses_of_current_user(client: TestClient):
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

    response = client.get(url="/expenses/", headers=headers)
    data: list[Any] = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["category_id"] == 1
    assert data[0]["amount"] == 1
    assert data[0]["description"] == "string"
    assert data[0]["spent_at"] == f"{date.today()}"
    assert data[0]["id"] == 1
    assert data[0]["user_id"] == 1
    assert data[0]["created_at"].startswith(date.today().isoformat())
    assert data[0]["updated_at"].startswith(date.today().isoformat())


def test_list_expenses_with_dates(client: TestClient):
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

    response = client.get(
        url=f"/expenses/?from_date={date.today()}&to_date={date.today()}",
        headers=headers,
    )
    data: list[Any] = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["category_id"] == 1
    assert data[0]["amount"] == 1
    assert data[0]["description"] == "string"
    assert data[0]["spent_at"] == f"{date.today()}"
    assert data[0]["id"] == 1
    assert data[0]["user_id"] == 1
    assert data[0]["created_at"].startswith(date.today().isoformat())
    assert data[0]["updated_at"].startswith(date.today().isoformat())


def test_list_expenses_from_date(client: TestClient):
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

    response = client.get(
        url=f"/expenses/?from_date={date.today()}",
        headers=headers,
    )
    data: list[Any] = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["category_id"] == 1
    assert data[0]["amount"] == 1
    assert data[0]["description"] == "string"
    assert data[0]["spent_at"] == f"{date.today()}"
    assert data[0]["id"] == 1
    assert data[0]["user_id"] == 1
    assert data[0]["created_at"].startswith(date.today().isoformat())
    assert data[0]["updated_at"].startswith(date.today().isoformat())


def test_list_expenses_to_date(client: TestClient):
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

    response = client.get(
        url=f"/expenses/?to_date={date.today()}",
        headers=headers,
    )
    data: list[Any] = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["category_id"] == 1
    assert data[0]["amount"] == 1
    assert data[0]["description"] == "string"
    assert data[0]["spent_at"] == f"{date.today()}"
    assert data[0]["id"] == 1
    assert data[0]["user_id"] == 1
    assert data[0]["created_at"].startswith(date.today().isoformat())
    assert data[0]["updated_at"].startswith(date.today().isoformat())


def test_list_expenses_of_another_user(client: TestClient):
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

    # Second user tries to access first user's expenses
    response = client.get(url="/expenses/", headers=second_user_headers)
    data: list[Any] = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 0


def test_list_expenses_unauthenticated(client: TestClient):
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

    response = client.get(url="/expenses/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

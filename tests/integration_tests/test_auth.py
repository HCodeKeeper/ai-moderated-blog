import pytest
from ninja_extra.testing import TestClient
from ninja_jwt.controller import schema as jwt_schema

from authentication.api import AuthController
from custom_users.schemas import UserOutSchema


@pytest.mark.django_db
def test_register_user_without_name(django_user_model):
    email = "user1@gmail.com"
    password = "password"
    client = TestClient(AuthController)
    response = client.post(
        "register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200
    UserOutSchema(**response.json())
    user = django_user_model.objects.get(email=email)
    assert user.check_password(password)
    assert user.first_name is None
    assert user.last_name is None


@pytest.mark.django_db
def test_register_user_with_name(django_user_model):
    email = "user1@gmail.com"
    password = "password"
    first_name = "John"
    last_name = "Doe"

    client = TestClient(AuthController)
    response = client.post(
        "register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    assert response.status_code == 200
    UserOutSchema(**response.json())
    user = django_user_model.objects.get(email=email)
    assert response.json()["id"] == user.id


@pytest.mark.django_db
def test_login(user, test_password):
    client = TestClient(AuthController)
    response = client.post(
        "login",
        json={
            "email": user.email,
            "password": test_password,
        },
    )

    assert response.status_code == 200
    jwt_schema.obtain_pair_schema.get_response_schema()(**response.json())
    assert "email" in response.json()
    assert "access" in response.json()
    assert "refresh" in response.json()
    assert response.json()["access"]
    assert response.json()["refresh"]


@pytest.mark.django_db
def test_login_wrong_password(user):
    client = TestClient(AuthController)
    response = client.post(
        "login",
        json={
            "email": user.email,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401

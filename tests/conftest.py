"""
Fixtures
"""

import pytest


@pytest.fixture
def test_password():
    return "password"


@pytest.fixture
def user(django_user_model, test_password):
    return django_user_model.objects.create_user(
        email="testuser@gmail.com", password=test_password, first_name="John", last_name="Doe"
    )

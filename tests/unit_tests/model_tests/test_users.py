import pytest
from django.db import IntegrityError

from custom_users.models import User


@pytest.mark.django_db(transaction=True)
def test_create_user():
    email = "user1@example.com"
    password = "1234"
    user = User.objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password) is True
    assert user.first_name is None
    assert user.last_name is None


@pytest.mark.django_db(transaction=True)
def test_user_set_full_name():
    email = "user1@example.com"
    password = "1234"
    first_name = "John"
    last_name = "Doe"
    user = User.objects.create_user(email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.check_password(password) is True


@pytest.mark.django_db(transaction=True)
def test_create_superuser():
    email = "admin@example.com"
    password = "1234"
    super_user = User.objects.create_superuser(email=email, password=password)

    assert super_user.email == email
    assert super_user.check_password(password) is True


@pytest.mark.django_db(transaction=True)
def test_create_user_duplicate_email_raises_exception():
    email = "admin@example.com"
    password = "1234"
    User.objects.create_user(email=email, password=password)

    with pytest.raises(IntegrityError):
        User.objects.create_user(email=email, password=password)

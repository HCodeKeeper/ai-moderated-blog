"""
Fixtures
"""

import random
from datetime import timedelta

import pytest
from django.utils import timezone
from faker import Faker
from ninja_extra.testing import TestClient as BaseTestClient
from ninja_jwt.tokens import RefreshToken

from posts.models import Comment, Post

faker = Faker()


class AuthenticatedTestClient(BaseTestClient):
    def __init__(self, *args, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    def request(self, method, path, data=None, json=None, **request_params):
        if self.token:
            headers = request_params.setdefault("headers", {})
            headers["Authorization"] = f"Bearer {self.token}"
        return super().request(method, path, data, json, **request_params)


@pytest.fixture
def test_password():
    return "password"


@pytest.fixture
def test_email():
    return "test@gmail.com"


@pytest.fixture
def user(django_user_model, test_password, test_email):
    return django_user_model.objects.create_user(
        email=test_email, password=test_password, first_name="John", last_name="Doe"
    )


@pytest.fixture
def jwt_for_admin_user(admin_user):

    return RefreshToken.for_user(admin_user)


@pytest.fixture
def jwt_for_user(user):

    return RefreshToken.for_user(user)


@pytest.fixture
def random_user(django_user_model, test_password):
    return django_user_model.objects.create_user(
        email=faker.email(), password=test_password, first_name=faker.first_name(), last_name=faker.last_name()
    )


@pytest.fixture
def generate_posts(user):
    posts = []
    for _ in range(20):
        post = Post(title=faker.sentence(), content=faker.text(), is_blocked=random.choice([True, False]), author=user)
        post.save()
        posts.append(post)
    return posts


@pytest.fixture
def fill_comments(generate_posts, random_user):
    all_comments = []
    for post in generate_posts:
        for _ in range(20):
            created_at = timezone.now() - timedelta(
                days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59)
            )
            comment = Comment(
                content=faker.text(),
                created_at=created_at,
                is_blocked=random.choice([True, False]),
                post=post,
                author=random_user,
            )
            comment.save()

            all_comments.append(comment)

    return all_comments

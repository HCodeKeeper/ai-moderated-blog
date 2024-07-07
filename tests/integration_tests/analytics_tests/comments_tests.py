from datetime import date, timedelta

import pytest

from analytics.api import CommentsAnalyticsAPI
from analytics.schemas.analytics import DailyCommentBlockedBreakdownSchema
from analytics.services.analytics import CommentAnalyticsService
from tests.conftest import AuthenticatedTestClient


# Write tests for comments analytics and test its validation
@pytest.fixture
def admin_client(jwt_for_admin_user):
    return AuthenticatedTestClient(CommentsAnalyticsAPI, token=jwt_for_admin_user.access_token)


@pytest.mark.django_db
def test_daily_breakdown_empty(admin_client):
    # Arrange
    client = admin_client
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Act
    response = client.get(f"/daily-breakdown?start_date={start_date_str}&end_date={end_date_str}")

    # Assert
    assert response.status_code == 200
    result = DailyCommentBlockedBreakdownSchema(**response.json())
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.total == 0
    assert result.total_active == 0
    assert result.total_blocked == 0
    assert len(result.daily_breakdown) == 0
    assert result.daily_breakdown == []


@pytest.mark.django_db
def test_daily_breakdown(admin_client, fill_comments):
    # Arrange
    client = admin_client
    start_date = date(2024, 1, 1)
    end_date = date.today()
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Act
    response = client.get(f"/daily-breakdown?start_date={start_date_str}&end_date={end_date_str}")

    # Assert
    assert response.status_code == 200
    result = DailyCommentBlockedBreakdownSchema(**response.json())
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.total == len(fill_comments)
    assert result.total_active is not None
    assert result.total_blocked is not None
    assert len(result.daily_breakdown) is not None


@pytest.mark.django_db
def test_daily_breakdown_end_date_before_start(admin_client):
    # Arrange
    client = admin_client
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Act
    response = client.get(f"/daily-breakdown?start_date={end_date_str}&end_date={start_date_str}")

    # Assert
    assert response.status_code == 400


@pytest.mark.django_db
def test_daily_breakdown_end_date_future(admin_client):
    # Arrange
    client = admin_client
    start_date = date(2024, 1, 1)
    end_date = date.today() + timedelta(days=1)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Act
    response = client.get(f"/daily-breakdown?start_date={start_date_str}&end_date={end_date_str}")

    # Assert
    assert response.status_code == 400


@pytest.mark.django_db
def test_daily_breakdown_start_date_future(admin_client):
    # Arrange
    client = admin_client
    start_date = date.today() + timedelta(days=1)
    end_date = date(2024, 1, 31)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Act
    response = client.get(f"/daily-breakdown?start_date={start_date_str}&end_date={end_date_str}")

    # Assert
    assert response.status_code == 400


@pytest.mark.django_db
def test_daily_breakdown_invalid_date_format(admin_client):
    client = admin_client

    assert client.get(f"/daily-breakdown?start_date={"04.04.2022"}&end_date={"04.05.2022"}").status_code == 422
    assert client.get(f"/daily-breakdown?start_date={"2022.04.04"}&end_date={"2022.04.05"}").status_code == 422
    assert client.get(f"/daily-breakdown?start_date={"str"}&end_date={"str"}").status_code == 422


@pytest.mark.django_db
def test_daily_breakdown_service_on_empty_db():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    service = CommentAnalyticsService()
    result = service.daily_breakdown(start_date, end_date)
    assert isinstance(result, DailyCommentBlockedBreakdownSchema)
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.total == 0
    assert result.total_active == 0
    assert result.total_blocked == 0
    assert len(result.daily_breakdown) == 0


@pytest.mark.django_db
def test_daily_breakdown_service(fill_comments):
    start_date = date(2024, 1, 1)
    end_date = date.today()

    service = CommentAnalyticsService()
    result = service.daily_breakdown(start_date, end_date)
    assert isinstance(result, DailyCommentBlockedBreakdownSchema)
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.total == len(fill_comments)
    assert result.total_active is not None
    assert result.total_blocked is not None
    assert len(result.daily_breakdown) is not None

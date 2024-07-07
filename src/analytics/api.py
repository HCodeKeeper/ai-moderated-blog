from datetime import date

from ninja_extra import ControllerBase, api_controller, http_get
from ninja_extra.exceptions import ParseError
from ninja_extra.permissions.common import IsAdminUser
from ninja_jwt.authentication import JWTAuth

from analytics.schemas.analytics import DailyCommentBlockedBreakdownSchema
from analytics.services.analytics import AbstractCommentAnalyticsService
from analytics.validators import validate_date_range

OLDEST_DATE = date(1970, 1, 1)  # The Unix epoch start date to use for all-time filtering


@api_controller(
    "analytics/comments", tags=["analytics", "comments-analytics"], auth=JWTAuth(), permissions=[IsAdminUser]
)
class CommentsAnalyticsAPI(ControllerBase):

    def __init__(self, analytics_service: AbstractCommentAnalyticsService):
        self.analytics_service = analytics_service

    @http_get("/daily-breakdown", response=DailyCommentBlockedBreakdownSchema)
    def daily_breakdown(self, request, start_date: date = None, end_date: date = None):
        if not start_date:
            start_date = OLDEST_DATE
        if not end_date:
            end_date = date.today()
        try:
            validate_date_range(start_date, end_date)
        except ValueError as e:
            raise ParseError(str(e)) from e

        return self.analytics_service.daily_breakdown(start_date, end_date)

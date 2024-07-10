from abc import ABC, abstractmethod
from datetime import date

from django.db.models import Count, QuerySet
from django.db.models.functions import ExtractWeekDay, TruncDate
from django.utils import timezone

from analytics.schemas.analytics import CommentBlockedBreakdownSchema, DailyCommentBlockedBreakdownSchema
from posts.models import Comment


class AbstractCommentAnalyticsService(ABC):

    @abstractmethod
    def daily_breakdown(self, start_date: date, end_date: date) -> DailyCommentBlockedBreakdownSchema:
        pass


class CommentAnalyticsService(AbstractCommentAnalyticsService):

    def __build_daily_query(self, base: QuerySet, is_blocked=None):
        """
        Helper function to build the daily query

        Args:
            base (QuerySet): The base query to filter and annotate upon. For example upon objects in a period of time.
            is_blocked (bool): The value of the is_blocked field to filter upon. If None, no filter is applied (any).
        """
        query = base

        if is_blocked is not None:
            query = query.filter(is_blocked=is_blocked)

        query = (
            query.annotate(date=TruncDate("created_at"))
            .annotate(day_of_week=ExtractWeekDay("date"))
            .values("date", "day_of_week")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        return query

    def daily_breakdown(self, start_date: date, end_date: date) -> DailyCommentBlockedBreakdownSchema:
        # Use aware
        start_datetime = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        end_datetime = timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time()))

        total_comments = Comment.objects.filter(created_at__range=(start_datetime, end_datetime))

        total_active_comments = total_comments.filter(is_blocked=False).count()
        total_blocked_comments = total_comments.filter(is_blocked=True).count()
        total_comments_count = total_comments.count()

        # Daily counts in the given period

        daily_active_posts = self.__build_daily_query(total_comments, is_blocked=False)

        daily_blocked_posts = self.__build_daily_query(total_comments, is_blocked=True)

        daily_comments = self.__build_daily_query(total_comments)

        daily_breakdown_list = []
        for daily_comment in daily_comments:
            date = daily_comment["date"]
            day_of_week = daily_comment["day_of_week"]
            total = daily_comment["count"]

            # Getting comment if created that day and get count, otherwise count is 0
            active_count = next((item for item in daily_active_posts if item["date"] == date), {}).get("count", 0)
            blocked_count = next((item for item in daily_blocked_posts if item["date"] == date), {}).get("count", 0)

            daily_breakdown_list.append(
                CommentBlockedBreakdownSchema(
                    date=date,
                    day_of_week=day_of_week,
                    total=total,
                    total_active=active_count,
                    total_blocked=blocked_count,
                )
            )

        return DailyCommentBlockedBreakdownSchema(
            start_date=start_date,
            end_date=end_date,
            total=total_comments_count,
            total_active=total_active_comments,
            total_blocked=total_blocked_comments,
            daily_breakdown=daily_breakdown_list,
        )

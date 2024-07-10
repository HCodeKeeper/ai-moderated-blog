from injector import Binder, Module

from analytics.services.analytics import AbstractCommentAnalyticsService, CommentAnalyticsService


class CommentsAnalyticsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AbstractCommentAnalyticsService, CommentAnalyticsService)

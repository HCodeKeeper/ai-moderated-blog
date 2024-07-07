from datetime import date
from typing import List

from ninja_schema import Schema
from pydantic import field_validator, root_validator

from analytics.validators import end_date_not_before_start_date, end_date_not_future, start_date_not_future


class CommentBlockedBreakdownSchema(Schema):
    date: date
    day_of_week: int
    total: int
    total_active: int
    total_blocked: int


class DailyCommentBlockedBreakdownSchema(Schema):
    start_date: date
    end_date: date
    total: int
    total_active: int
    total_blocked: int
    daily_breakdown: List[CommentBlockedBreakdownSchema]

    @field_validator("start_date")
    def start_date_not_future(cls, v):
        v = start_date_not_future(v)
        return v

    @field_validator("end_date")
    def end_date_not_future(cls, v):
        v = end_date_not_future(v)
        return v

    @root_validator(skip_on_failure=True)
    def end_date_not_before_start_date(cls, values):
        end_date_not_before_start_date(values["start_date"], values["end_date"])
        return values

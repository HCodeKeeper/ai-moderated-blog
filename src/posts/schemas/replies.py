from typing import Optional

from ninja import ModelSchema, Schema
from pydantic import field_validator

from posts.models import Reply


class ParentReplyOutSchema(ModelSchema):
    id: int
    content: str

    class Meta:
        model = Reply
        fields = ["id"]


class ReplyOutSchema(ModelSchema):
    parent_reply: Optional[ParentReplyOutSchema] = None

    class Meta:
        model = Reply
        fields = "__all__"


class ReplyCreateSchema(Schema):
    author_id: int
    comment_id: int
    parent_reply_id: Optional[int] = None
    content: str

    @field_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class ReplyUpdateSchema(Schema):
    content: str

    @field_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class AIReplyCreateSchema(Schema):
    comment_id: int
    content: str

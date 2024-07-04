from typing import Optional

from ninja import ModelSchema, Schema

from posts.models import Reply


class ParentReplySchema(ModelSchema):
    id: int
    content: str

    class Meta:
        model = Reply
        fields = ["id"]


class ReplyOutSchema(ModelSchema):
    parent_reply: Optional[ParentReplySchema] = None

    class Meta:
        model = Reply
        fields = "__all__"


class ReplyCreateSchema(Schema):
    author_id: int
    comment_id: int
    parent_reply_id: Optional[int] = None
    content: str


class ReplyUpdateSchema(Schema):
    content: str


class AIReplyCreateSchema(Schema):
    parent_reply_id: Optional[int] = None
    comment_id: int
    content: str

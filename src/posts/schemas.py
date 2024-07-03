from typing import Optional

from ninja import ModelSchema, Schema

from custom_users.models import User
from posts.models import MAX_COMMENT_LENGTH, MIN_COMMENT_LENGTH, Comment, Post, Reply


class CommentValidationMixin:
    def validate_content(self, value):
        content_length = len(value)
        if content_length < MIN_COMMENT_LENGTH:
            raise ValueError(f"Content is too short: {content_length}")
        elif len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Content is too long: {content_length}")
        return value


class ReplyValidationMixin:
    def validate_content(self, value):
        content_length = len(value)
        if content_length < MIN_COMMENT_LENGTH:
            raise ValueError(f"Content is too short: {content_length}")
        elif len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Content is too long: {content_length}")
        return value


class AuthorSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class PostOutSchema(ModelSchema):
    id: int
    author: AuthorSchema

    class Meta:
        model = Post
        fields = "__all__"


class PostUpdateSchema(ModelSchema):
    class Meta:
        model = Post
        exclude = ["author", id]


class PostCreateSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentOutSchema(ModelSchema):
    author: AuthorSchema

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSchema(CommentValidationMixin, Schema):
    author_id: int
    post_id: int
    content: str


class CommentUpdateSchema(CommentValidationMixin, Schema):
    id: int
    content: str


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


class ReplyCreateSchema(ReplyValidationMixin, Schema):
    author_id: int
    comment_id: int
    parent_reply_id: Optional[int] = None
    content: str


class AIReplyCreateSchema(ReplyValidationMixin, Schema):
    parent_reply_id: Optional[int] = None
    comment_id: int
    content: str


class ReplyUpdateSchema(ReplyValidationMixin, Schema):
    id: int
    content: str

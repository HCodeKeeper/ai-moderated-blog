from ninja import ModelSchema
from ninja_schema import Schema
from pydantic import Field, field_validator

from posts.exceptions import InvalidContentLengthError
from posts.models import Comment
from posts.schemas.general import AuthorSchema
from posts.validators import validate_comment_length


class CommentOutSchema(ModelSchema):
    author: AuthorSchema

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSchema(Schema):
    post_id: int = Field(ge=1)
    content: str

    @field_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    @field_validator("content", check_fields=False)
    def content_valid_length(cls, v):
        try:
            validate_comment_length(v.strip())
        except InvalidContentLengthError as e:
            raise ValueError(e.message)
        return v


class CommentUpdateSchema(Schema):
    content: str

    @field_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    @field_validator("content", check_fields=False)
    def content_valid_length(cls, v):
        try:
            validate_comment_length(v.strip())
        except InvalidContentLengthError as e:
            raise ValueError(e.message)
        return v

from ninja import ModelSchema, Schema
from ninja_schema import model_validator

from posts.models import Comment
from posts.schemas.general import AuthorSchema


class CommentOutSchema(ModelSchema):
    author: AuthorSchema

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSchema(Schema):
    author_id: int
    post_id: int
    content: str

    @model_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class CommentUpdateSchema(Schema):
    content: str

    @model_validator("content", check_fields=False)
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v

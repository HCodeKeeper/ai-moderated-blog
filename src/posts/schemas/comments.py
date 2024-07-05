from ninja import ModelSchema, Schema

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


class CommentUpdateSchema(Schema):
    content: str

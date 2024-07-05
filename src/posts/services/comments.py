from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from api.services import AbstractService
from posts.exceptions import EntityDoesNotExistError
from posts.models import Comment, Post
from posts.schemas.comments import CommentCreateSchema, CommentUpdateSchema
from posts.validators import validate_profanity


class AbstractCommentsService(AbstractService, ABC):
    @abstractmethod
    def list_by_post(self, post_id: int):
        pass


class CommentsService(AbstractCommentsService):
    def __init__(self):
        super().__init__()

    def list(self):
        return Comment.objects.all()

    def list_by_post(self, post_id: int):
        post = Post.objects.get(id=post_id)
        return post.comment_set.all()

    def get(self, _id: int):
        return Comment.objects.get(id=_id)

    def create(self, schema: CommentCreateSchema):
        validate_profanity([schema.content])

        try:
            Post.objects.get(id=schema.post_id)
        except Post.DoesNotExist as e:
            raise EntityDoesNotExistError(entity_name="Post", entity_id=schema.post_id) from e
        try:
            get_user_model().objects.get(id=schema.author_id)
        except get_user_model().DoesNotExist as e:
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id) from e

        return Comment.objects.create(**schema.dict())

    def update(self, _id: int, schema: CommentUpdateSchema):
        comment = Comment.objects.get(id=_id)

        validate_profanity([schema.content])

        comment_data_dict = schema.dict()
        for key, value in comment_data_dict.items():
            setattr(comment, key, value)
        comment.save()

    def delete(self, _id: int):
        comment = Comment.objects.get(id=_id)
        comment.delete()

from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError
from posts.models import Comment, Post
from posts.schemas.comments import CommentCreateSchema, CommentUpdateSchema
from posts.services.profanity import detect_profanity
from posts.services.services import AbstractService
from posts.validators import validate_comment_length, validate_profanity


class AbstractCommentsService(AbstractService, ABC):
    @abstractmethod
    def list_by_post(self, post_id: int):
        pass

    @abstractmethod
    def get_inactive(self, _id: int):
        pass

    @abstractmethod
    def list_active(self):
        pass

    @abstractmethod
    def list_active_by_post(self, post_id: int):
        pass

    @abstractmethod
    def list_inactive_by_post(self, post_id: int):
        pass


class CommentsService(AbstractCommentsService):

    def __init__(self):
        super().__init__()

    def list_active(self):
        return Comment.objects.filter(is_blocked=False)

    def list(self):
        return Comment.objects.all()

    def list_active_by_post(self, post_id: int):
        if not Post.objects.filter(id=post_id).exists():
            raise Post.DoesNotExist(f"Post with id {post_id} does not exist.")

        post = Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_blocked=False))
        ).get(id=post_id)
        return post.comment_set.all()

    def list_by_post(self, post_id: int):
        if not Post.objects.filter(id=post_id).exists():
            raise Post.DoesNotExist(f"Post with id {post_id} does not exist.")

        post = Post.objects.prefetch_related("comment_set").get(id=post_id)
        return post.comment_set.all()

    def list_inactive_by_post(self, post_id: int):
        if not Post.objects.filter(id=post_id).exists():
            raise Post.DoesNotExist(f"Post with id {post_id} does not exist.")

        post = Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_blocked=True))
        ).get(id=post_id)
        return post.comment_set.all()

    def get(self, _id: int):
        return Comment.objects.get(id=_id, is_blocked=False)

    def get_inactive(self, _id: int):
        return Comment.objects.get(id=_id, is_blocked=True)

    def create(self, schema: CommentCreateSchema):
        validate_comment_length(schema.content)
        has_profanity = detect_profanity([schema.content])

        if not Post.objects.filter(id=schema.post_id, is_blocked=False).exists():
            raise EntityDoesNotExistError(entity_name="Post", entity_id=schema.post_id)

        if not get_user_model().objects.filter(id=schema.author_id).exists():
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id)

        comment = Comment.objects.create(
            post_id=schema.post_id, author_id=schema.author_id, content=schema.content, is_blocked=has_profanity
        )
        if has_profanity:
            raise ContentContainsProfanityError()
        return comment

    def update(self, _id: int, schema: CommentUpdateSchema):
        comment = Comment.objects.get(id=_id, is_blocked=False)

        validate_comment_length(schema.content)
        validate_profanity([schema.content])

        comment_data_dict = schema.dict()
        for key, value in comment_data_dict.items():
            setattr(comment, key, value)

        comment.save()

    def delete(self, _id: int):
        comment = Comment.objects.get(id=_id, is_blocked=False)
        comment.delete()

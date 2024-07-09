from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db import transaction

from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError
from posts.models import AutoReplyConfig, Post
from posts.schemas.posts import PostCreateSchema, PostUpdateSchema
from posts.services.profanity import detect_profanity
from posts.services.services import AbstractService
from posts.validators import validate_post_title, validate_profanity


class AbstractPostsService(AbstractService, ABC):
    @abstractmethod
    def get_inactive(self, _id: int):
        pass

    @abstractmethod
    def list_active(self):
        pass


class PostsService(AbstractPostsService):
    def __init__(self):
        super().__init__()

    def list(self):
        return Post.objects.all()

    def list_active(self):
        return Post.objects.filter(is_blocked=False)

    def get(self, _id: int):
        return Post.objects.get(id=_id, is_blocked=False)

    def get_inactive(self, _id: int):
        return Post.objects.get(id=_id, is_blocked=True)

    def create(self, schema: PostCreateSchema):
        validate_post_title(schema.title)
        has_profanity = detect_profanity([schema.title, schema.content])

        if not get_user_model().objects.filter(id=schema.author_id).exists():
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id)

        post_dict = schema.dict()
        auto_reply_dict = post_dict["auto_reply_config"]
        del post_dict["auto_reply_config"]
        with transaction.atomic():
            post = Post.objects.create(**post_dict, is_blocked=has_profanity)
            if auto_reply_dict:
                AutoReplyConfig.objects.create(post_id=post.id, delay_secs=auto_reply_dict["delay_secs"])

        if has_profanity:
            raise ContentContainsProfanityError()
        return post

    def update(self, _id: int, schema: PostUpdateSchema):
        post = Post.objects.get(id=_id, is_blocked=False)

        validate_post_title(schema.title)
        validate_profanity([schema.content, schema.title])

        post_data_dict = schema.dict()
        for key, value in post_data_dict.items():
            setattr(post, key, value)

        post.save()

    def delete(self, _id: int):
        post = Post.objects.get(id=_id, is_blocked=False)
        post.delete()

from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from posts.exceptions import EntityDoesNotExistError
from posts.models import Post
from posts.schemas.posts import PostCreateSchema, PostUpdateSchema
from posts.validators import validate_post_title, validate_profanity


class AbstractService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, schema):
        pass

    @abstractmethod
    def get(self, _id: int):
        pass

    @abstractmethod
    def update(self, _id: int, schema):
        pass

    @abstractmethod
    def delete(self, _id: int):
        pass


class AbstractPostsService(AbstractService, ABC):
    pass


class PostsService(AbstractPostsService):
    def __init__(self):
        super().__init__()

    def list(self):
        return Post.objects.all()

    def get(self, _id: int):
        return Post.objects.get(id=_id)

    def create(self, schema: PostCreateSchema):
        validate_post_title(schema.title)
        validate_profanity([schema.title, schema.content])

        try:
            get_user_model().objects.get(id=schema.author_id)
        except get_user_model().DoesNotExist as e:
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id) from e

        return Post.objects.create(**schema.dict())

    def update(self, _id: int, schema: PostUpdateSchema):
        post = Post.objects.get(id=_id)

        validate_post_title(schema.title)
        validate_profanity([schema.title, schema.content])

        post_data_dict = schema.dict()
        for key, value in post_data_dict.items():
            setattr(post, key, value)

        post.save()

    def delete(self, _id: int):
        post = Post.objects.get(id=_id)
        post.delete()

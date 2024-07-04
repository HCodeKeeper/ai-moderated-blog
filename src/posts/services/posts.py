from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError, InvalidTitleLengthError
from posts.models import MAX_TITLE_LENGTH, MIN_TITLE_LENGTH, Post
from posts.schemas.posts import PostCreateSchema, PostUpdateSchema
from posts.services.profanity import detect_profanity


class AbstractPostsService(ABC):
    def __init__(self):
        pass

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


class PostsService(AbstractPostsService):
    def __init__(self):
        super().__init__()

    def _validate_title(self, title: str):
        title_length = len(title)
        if title_length < MIN_TITLE_LENGTH:
            raise InvalidTitleLengthError(length=title_length)
        elif title_length > MAX_TITLE_LENGTH:
            raise InvalidTitleLengthError(length=title_length)
        return title

    def _validate_profanity(self, contents: [str]):
        if detect_profanity(contents):
            raise ContentContainsProfanityError()

    def list(self):
        return Post.objects.all()

    def get(self, _id: int):
        return Post.objects.get(id=_id)

    def create(self, schema: PostCreateSchema):
        self._validate_title(schema.title)
        self._validate_profanity([schema.title, schema.content])

        try:
            get_user_model().objects.get(id=schema.author_id)
        except get_user_model().DoesNotExist as e:
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id) from e

        return Post.objects.create(**schema.dict())

    def update(self, _id: int, schema: PostUpdateSchema):
        post = Post.objects.get(id=_id)
        self._validate_title(schema.title)
        self._validate_profanity([schema.title, schema.content])

        post_data_dict = schema.dict()
        for key, value in post_data_dict.items():
            setattr(post, key, value)
        post.save()

    def delete(self, _id: int):
        post = Post.objects.get(id=_id)
        post.delete()

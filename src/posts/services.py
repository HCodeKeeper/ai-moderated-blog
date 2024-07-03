from abc import ABC, abstractmethod

from posts.schemas import PostCreateSchema, PostOutSchema


class AbstractPostService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create(self, author_id: int, schema: PostCreateSchema):
        pass

    @abstractmethod
    def get_active(self, _id: int):
        pass

    @abstractmethod
    def get(self, _id: int):
        pass

    @abstractmethod
    def update(self, schema: PostOutSchema):
        pass

    @abstractmethod
    def delete(self, _id: int):
        pass

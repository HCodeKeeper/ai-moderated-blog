from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def list_active(self):
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

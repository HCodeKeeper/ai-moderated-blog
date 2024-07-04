from injector import Binder, Module

from posts.services.posts import AbstractPostsService, PostsService


class PostsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AbstractPostsService, PostsService)

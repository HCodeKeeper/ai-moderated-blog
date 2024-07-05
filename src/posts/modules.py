from injector import Binder, Module

from posts.services.comments import AbstractCommentsService, CommentsService
from posts.services.posts import AbstractPostsService, PostsService


class PostsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AbstractPostsService, PostsService)


class CommentsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AbstractCommentsService, CommentsService)

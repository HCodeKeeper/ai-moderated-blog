from ninja_extra import NinjaExtraAPI

from authentication.api import AuthController
from custom_users.api import UsersController
from posts.api import CommentsController, PostsController, RepliesController

api = NinjaExtraAPI(title="AI Moderated Blog API")

api.register_controllers(
    AuthController,
    UsersController,
    PostsController,
    CommentsController,
    RepliesController,
)

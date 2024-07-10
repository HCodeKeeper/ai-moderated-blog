from ninja import Swagger
from ninja_extra import NinjaExtraAPI

from analytics.api import CommentsAnalyticsAPI
from authentication.api import AuthController
from custom_users.api import UsersController
from posts.api import CommentsController, PostsController, RepliesController

api = NinjaExtraAPI(title="AI Moderated Blog API", docs=Swagger(settings={"persistAuthorization": True}))

api.register_controllers(
    AuthController,
    UsersController,
    PostsController,
    CommentsController,
    RepliesController,
    CommentsAnalyticsAPI,
)

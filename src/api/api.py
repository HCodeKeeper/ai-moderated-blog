from ninja_extra import NinjaExtraAPI

from auth.api import AuthController
from custom_users.api import UsersController

api = NinjaExtraAPI(title="AI Moderated Blog API")

api.register_controllers(
    AuthController,
    UsersController,
)

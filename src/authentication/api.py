from django.contrib.auth import get_user_model
from ninja_extra import api_controller, http_post
from ninja_jwt.controller import TokenObtainPairController, TokenVerificationController
from ninja_jwt.controller import schema as jwt_schema

from authentication.schemas import RegisterUserSchema
from custom_users.schemas import UserOutSchema


@api_controller("auth", tags=["Auth"])
class AuthController(TokenObtainPairController, TokenVerificationController):
    """
    Controller for user registration, login and jwt operations

    Methods:
    - register_user: Register a new user
    - login: Obtain a new jwt token
    - refresh_token: Refresh a jwt token
    - verify_token: Verify a jwt token
    """

    @http_post(path="register", response=UserOutSchema)
    def register_user(self, user_data: RegisterUserSchema):
        user = get_user_model().objects.create_user(**user_data.dict())
        return user

    @http_post(
        path="login",
        response=jwt_schema.obtain_pair_schema.get_response_schema(),
        url_name="token_obtain_pair",
    )
    def obtain_token(self, user_token: jwt_schema.obtain_pair_schema):
        return super().obtain_token(user_token)

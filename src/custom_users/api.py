from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja_extra import ControllerBase, api_controller, http_delete, http_get, http_put, status
from ninja_extra.pagination import paginate
from ninja_extra.permissions.common import IsAdminUser
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth

from custom_users.permissions import IsSelf
from custom_users.schemas import UpdateUserSchema, UserOutSchema


@api_controller("users/")
class UsersController(ControllerBase):
    @http_get("{int:user_id}", response=UserOutSchema)
    def get_user(self, request, user_id: int):
        user = get_object_or_404(get_user_model(), id=user_id)
        return user

    @http_put(response=UserOutSchema, permissions=[IsSelf | IsAdminUser], auth=JWTAuth())
    def update_user(self, user_data: UpdateUserSchema):
        user = get_object_or_404(get_user_model(), id=user_data.id)
        user_data_dict = user_data.dict()
        del user_data_dict["id"]
        for key, value in user_data_dict.items():
            setattr(user, key, value)
        user.save()
        return user

    @http_delete(path="{int:user_id}", permissions=[IsSelf | IsAdminUser], auth=JWTAuth())
    def delete_user(self, user_id: int):
        user = get_object_or_404(get_user_model(), id=user_id)
        user.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)

    @http_get("me", response=UserOutSchema, auth=JWTAuth())
    def get_me(self, request):
        return request.user

    @http_get(response=NinjaPaginationResponseSchema[UserOutSchema])
    @paginate()
    def list_users(self, request):
        return get_user_model().objects.all()

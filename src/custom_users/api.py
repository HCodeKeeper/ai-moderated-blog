from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router

from custom_users.schemas import UserOutSchema

router = Router()


@router.get("/{int:user_id}", response=UserOutSchema)
def get_user(request, user_id: int):
    user = get_object_or_404(get_user_model(), id=user_id)
    return user

from typing import Optional

from ninja import ModelSchema, Schema

from custom_users.models import User


class UserOutSchema(Schema):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

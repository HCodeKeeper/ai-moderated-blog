from ninja import ModelSchema

from custom_users.models import User


class RegisterUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        fields_optional = ["first_name", "last_name"]

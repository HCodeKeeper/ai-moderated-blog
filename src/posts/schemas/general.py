from ninja import ModelSchema

from custom_users.models import User


class AuthorSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from custom_users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for ai_moderated_blog.
    """

    username = None
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    email = EmailField(
        _("email address"),
        unique=True,
        default=None,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

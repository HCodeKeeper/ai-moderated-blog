from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from custom_users.managers import UserManager

EMAIL_MIN_LENGTH = 3


class User(AbstractUser):
    """
    Default custom user model for ai_moderated_blog.
    """

    # First and last name do not cover name patterns around the globe
    username = CharField(_("username"), max_length=64, unique=True, default=None)
    first_name = None
    last_name = None
    email = EmailField(
        _("email address"),
        unique=True,
        validators=[
            MinLengthValidator(
                EMAIL_MIN_LENGTH,
                f"the field must contain at least {EMAIL_MIN_LENGTH} characters",
            )
        ],
        max_length=255,
        default=None,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

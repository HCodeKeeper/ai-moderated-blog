from typing import Any

from django.http import HttpRequest
from ninja_extra import permissions
from ninja_extra.controllers import ControllerBase


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: "ControllerBase") -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: HttpRequest, controller: "ControllerBase", obj: Any) -> bool:
        return request.user == obj.author

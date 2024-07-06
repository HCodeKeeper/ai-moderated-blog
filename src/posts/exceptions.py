from typing import Dict, List, Optional, Union

from ninja_extra import status
from ninja_extra.exceptions import APIException, ValidationError

import posts.models


class ResourceWithoutAuthorCreationError(ValidationError):
    def __init__(self, message="A resource must have an author."):
        self.message = message
        super().__init__(self.message)


class PostWithoutAuthorCreationError(ValidationError):
    def __init__(self, message="A post must have an author."):
        self.message = message
        super().__init__(self.message)


class CommentWithoutAuthorCreationError(ValidationError):
    def __init__(self, message="A comment must have an author."):
        self.message = message
        super().__init__(self.message)


class AnonymousReplyError(ValidationError):
    def __init__(self, message="A reply must have an author or be marked as AI-generated."):
        self.message = message
        super().__init__(self.message)


class SelfReplyingError(ValidationError):
    def __init__(self, message="A reply cannot be its own parent."):
        self.message = message
        super().__init__(self.message)


class InvalidContentLengthError(ValidationError):
    def __init__(self, length=None, _min=None, _max=None, message=None):
        self.max = _min
        self.min = _max
        self.length = length
        self.message = message or f"Content must be between {self.min} and {self.max} characters long."

        if self.length:
            self.message += f" | Received: {self.length}"

        super().__init__(self.message)


class InvalidTitleLengthError(InvalidContentLengthError):
    def __init__(self, length=None, message=None):
        self.max = posts.models.MAX_TITLE_LENGTH
        self.min = posts.models.MIN_TITLE_LENGTH
        self.length = length
        self.message = message or f"Title must be between {self.min} and {self.max} characters long."

        if self.length:
            self.message += f" | Received: {self.length}"

        super().__init__(self.length, self.min, self.max, self.message)


class ContentContainsProfanityError(ValidationError):
    def __init__(self, message="Content contains profanity."):
        self.message = message
        super().__init__(self.message)


class EntityDoesNotExistError(ValidationError):
    def __init__(self, entity_name: str, entity_id: id, message=None):
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.message = message or f"{self.entity_name} with id {self.entity_id} does not exist."
        super().__init__(self.message)


class InvalidRequestBodyError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Invalid request body."

    def __init__(
        self,
        detail: Optional[Union[List, Dict, "ErrorDetail", str]] = None,  # noqa
        code: Optional[Union[str, int]] = None,
    ) -> None:
        self.default_detail = detail or self.default_detail
        super().__init__(detail=self.default_detail, code=code or self.status_code)


class RelatedObjectDoesNotExistAPIError(InvalidRequestBodyError):
    def __init__(self, entity_name: str, entity_id: int, message=None):
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.default_detail = (
            "Related object {entity_name} with id {entity_id} does not exist.".format(
                entity_name=self.entity_name, entity_id=self.entity_id
            )
            or self.default_detail
        )
        super().__init__(detail=message or self.default_detail)


class ContentContainsProfanityAPIError(InvalidRequestBodyError):
    def __init__(self, message="Content contains profanity."):
        self.message = message
        super().__init__(detail=self.message)

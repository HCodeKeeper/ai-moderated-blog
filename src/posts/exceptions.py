from ninja_extra.exceptions import ValidationError

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


class InvalidTitleLengthError(ValidationError):
    def __init__(self, length=None, message=None):
        self.max = posts.models.MAX_TITLE_LENGTH
        self.min = posts.models.MIN_TITLE_LENGTH
        self.length = length
        self.message = message or f"Title must be between {self.min} and {self.max} characters long."

        if self.length:
            self.message += f" | Received: {self.length}"

        super().__init__(self.message)


class ContentContainsProfanityError(ValidationError):
    def __init__(self, message="Content contains profanity."):
        self.message = message
        super().__init__(self.message)


class EntityDoesNotExistError(ValidationError):
    def __init__(self, entity_name: str, entity_id: id, message=None):
        self.message = message or f"{entity_name} with id {entity_id} does not exist."
        super().__init__(self.message)

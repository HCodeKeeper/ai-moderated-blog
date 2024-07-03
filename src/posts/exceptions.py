from django.core.exceptions import ValidationError


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

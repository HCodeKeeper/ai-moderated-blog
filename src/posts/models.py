from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField

from posts.exceptions import (
    AnonymousReplyError,
    CommentWithoutAuthorCreationError,
    PostWithoutAuthorCreationError,
    SelfReplyingError,
)

MIN_COMMENT_LENGTH = 1
MAX_COMMENT_LENGTH = 500
MIN_TITLE_LENGTH = 5
MAX_TITLE_LENGTH = 100


class Post(models.Model):
    title = CharField(max_length=MAX_TITLE_LENGTH, validators=[MinLengthValidator(MIN_TITLE_LENGTH)])
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def __validate_author_exists_on_creation(self):
        if self.author is None:
            raise PostWithoutAuthorCreationError()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__validate_author_exists_on_creation()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)


class Comment(models.Model):
    content = CharField(max_length=500, validators=[MinLengthValidator(MIN_COMMENT_LENGTH)])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content[:10]

    def __validate_author_exists_on_creation(self):
        if self.author is None:
            raise CommentWithoutAuthorCreationError()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__validate_author_exists_on_creation()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)


class Reply(models.Model):
    content = models.TextField(validators=[MinLengthValidator(MIN_COMMENT_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="replies")
    parent_reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child_replies", null=True, blank=True
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        if self.is_ai_generated:
            return f"AI-generated reply on {self.comment}"
        return f"Reply by {self.author} on {self.comment}"

    def save(self, *args, **kwargs):
        if self.author is None and not self.is_ai_generated:
            raise AnonymousReplyError()
        if self.parent_reply_id and self.parent_reply_id == self.id:
            raise SelfReplyingError()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)

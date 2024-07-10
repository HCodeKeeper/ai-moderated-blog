from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError
from posts.models import Comment, Reply
from posts.schemas.replies import AIReplyCreateSchema, ReplyCreateSchema, ReplyUpdateSchema
from posts.services.profanity import detect_profanity
from posts.services.services import AbstractService
from posts.validators import validate_comment_length, validate_profanity


class AbstractRepliesService(AbstractService, ABC):
    @abstractmethod
    def list_by_comment(self, comment_id: int):
        pass

    @abstractmethod
    def get_inactive(self, _id: int):
        pass

    @abstractmethod
    def list_active(self):
        pass

    @abstractmethod
    def list_active_by_comment(self, comment_id: int):
        pass

    @abstractmethod
    def list_inactive_by_comment(self, comment_id: int):
        pass


class RepliesService(AbstractRepliesService):

    def __init__(self):
        super().__init__()

    def list_active(self):
        return Reply.objects.filter(is_blocked=False)

    def list(self):
        return Reply.objects.all()

    def list_active_by_comment(self, comment_id: int):
        if not Comment.objects.filter(id=comment_id).exists():
            raise Comment.DoesNotExist(f"Comment with id {comment_id} does not exist.")

        comment = Comment.objects.prefetch_related(
            Prefetch("replies", queryset=Reply.objects.filter(is_blocked=False))
        ).get(id=comment_id)
        return comment.replies.all()

    def list_by_comment(self, comment_id: int):
        if not Comment.objects.filter(id=comment_id).exists():
            raise Comment.DoesNotExist(f"Comment with id {comment_id} does not exist.")
        comment = Comment.objects.prefetch_related("replies").get(id=comment_id)
        return comment.replies.all()

    def list_inactive_by_comment(self, comment_id: int):
        if not Comment.objects.filter(id=comment_id).exists():
            raise Comment.DoesNotExist(f"Comment with id {comment_id} does not exist.")

        comment = Comment.objects.prefetch_related(
            Prefetch("replies", queryset=Reply.objects.filter(is_blocked=True))
        ).get(id=comment_id)
        return comment.replies.all()

    def get(self, _id: int):
        return Reply.objects.get(id=_id, is_blocked=False)

    def get_inactive(self, _id: int):
        return Reply.objects.get(id=_id, is_blocked=True)

    def create(self, schema: ReplyCreateSchema):
        validate_comment_length(schema.content)
        has_profanity = detect_profanity([schema.content])

        if not Comment.objects.filter(id=schema.comment_id, is_blocked=False).exists():
            raise EntityDoesNotExistError(entity_name="Comment", entity_id=schema.comment_id)

        if not get_user_model().objects.filter(id=schema.author_id).exists():
            raise EntityDoesNotExistError(entity_name="Author", entity_id=schema.author_id)

        if schema.parent_reply_id:
            if not Reply.objects.filter(id=schema.parent_reply_id, is_blocked=False).exists():
                raise EntityDoesNotExistError(entity_name="Parent Reply", entity_id=schema.parent_reply_id)

        reply = Reply.objects.create(
            comment_id=schema.comment_id,
            author_id=schema.author_id,
            content=schema.content,
            is_blocked=has_profanity,
            parent_reply_id=schema.parent_reply_id,
        )
        if has_profanity:
            raise ContentContainsProfanityError()
        return reply

    def update(self, _id: int, schema: ReplyUpdateSchema):
        reply = Reply.objects.get(id=_id, is_blocked=False)

        validate_comment_length(schema.content)
        validate_profanity([schema.content])

        reply_data_dict = schema.dict()
        for key, value in reply_data_dict.items():
            setattr(reply, key, value)

        reply.save()

    def delete(self, _id: int):
        reply = Reply.objects.get(id=_id, is_blocked=False)
        reply.delete()

    def create_ai_reply(self, schema: AIReplyCreateSchema):
        validate_comment_length(schema.content)

        if not Comment.objects.filter(id=schema.comment_id, is_blocked=False).exists():
            raise EntityDoesNotExistError(entity_name="Comment", entity_id=schema.comment_id)

        reply = Reply.objects.create(
            comment_id=schema.comment_id, content=schema.content, is_blocked=False, is_ai_generated=True
        )
        return reply

from logging import getLogger

from celery import shared_task
from django.db import IntegrityError

from posts.models import Comment, Post, Reply
from posts.schemas.comments import CommentOutSchema
from posts.schemas.posts import PostOutSchema
from posts.services.strategies.ai import gemini_response_strategy

logger = getLogger(__name__)


@shared_task
def generate_ai_reply_task(post_id: int, comment_id: int):
    """
    Generates and saves an AI reply for the given comment in the database.
    Naively considers that reply will be received instantly.
    """
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        logger.error(f"Comment {comment_id} was deleted before replied was created")
        return
    post_schema = PostOutSchema.from_orm(Post.objects.get(id=post_id))
    comment_schema = CommentOutSchema.from_orm(comment)
    reply = gemini_response_strategy.get_personalized_response(post_schema, comment_schema)
    try:
        Reply.objects.create(content=reply, comment_id=comment_id, is_ai_generated=True)
    except IntegrityError as e:
        logger.error(f"Error creating reply: {e}")
        raise e

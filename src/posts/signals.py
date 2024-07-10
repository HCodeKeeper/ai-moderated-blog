from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import AutoReplyConfig, Comment
from posts.schemas.comments import CommentOutSchema
from posts.schemas.posts import PostOutSchema
from posts.tasks.ai_tasks import generate_ai_reply_task


@receiver(post_save, sender=Comment)
def trigger_auto_reply_task(sender, instance: Comment, created, **kwargs):
    if created:
        comment_schema = CommentOutSchema.from_orm(instance)
        post_schema = PostOutSchema.from_orm(instance.post)
        try:
            auto_reply_config = AutoReplyConfig.objects.get(post_id=post_schema.id)
        except AutoReplyConfig.DoesNotExist:
            return
        generate_ai_reply_task.apply_async(
            args=[post_schema.id, comment_schema.id], countdown=auto_reply_config.delay_secs
        )

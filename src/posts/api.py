from django.shortcuts import get_object_or_404
from ninja_extra import ControllerBase, api_controller, http_delete, http_get, http_post, http_put, paginate, status
from ninja_extra.permissions.common import IsAdminUser
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth

from api.schemas import DetailSchema
from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError, InvalidTitleLengthError
from posts.models import Comment, Post, Reply
from posts.permissions import IsAuthor
from posts.schemas.comments import CommentCreateSchema, CommentOutSchema, CommentUpdateSchema
from posts.schemas.posts import PostCreateSchema, PostOutSchema, PostUpdateSchema
from posts.schemas.replies import ReplyCreateSchema, ReplyOutSchema, ReplyUpdateSchema
from posts.services.posts import AbstractPostsService


@api_controller("posts", tags=["posts"])
class PostsController(ControllerBase):

    def __init__(self, posts_service: AbstractPostsService):
        self.posts_service = posts_service

    @http_get(response=NinjaPaginationResponseSchema[PostOutSchema])
    @paginate()
    def list_posts(self, request):
        """
        List all posts

        """
        return self.posts_service.list()

    @http_get("{int:post_id}", response=PostOutSchema)
    def get_post(self, request, post_id: int):
        try:
            return self.posts_service.get(post_id)
        except Post.DoesNotExist:
            return self.create_response(
                {"detail": f"Post not found | id: {post_id}"}, status_code=status.HTTP_404_NOT_FOUND
            )

    @http_post(
        response={
            200: PostOutSchema,
            201: PostOutSchema,
            400: DetailSchema,
            422: DetailSchema,
        },
        auth=JWTAuth(),
    )
    def create_post(self, data: PostCreateSchema):
        try:
            return self.posts_service.create(data)
        except (InvalidTitleLengthError, ContentContainsProfanityError) as e:
            return 422, {"detail": e.message}
        except EntityDoesNotExistError as e:
            return 422, {"detail": e.message}

    @http_put(
        "{int:post_id}",
        response={
            200: PostOutSchema,
            422: DetailSchema,
        },
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def update_post(self, post_id: int, data: PostUpdateSchema):
        try:
            self.posts_service.update(post_id, data)
        except (InvalidTitleLengthError, ContentContainsProfanityError) as e:
            return 422, {"detail": e.message}
        except Post.DoesNotExist:
            return self.create_response(
                {"detail": f"Post not found | id: {post_id}"}, status_code=status.HTTP_404_NOT_FOUND
            )
        post = get_object_or_404(Post, id=post_id)
        return post

    @http_delete("{int:post_id}", permissions=[IsAuthor | IsAdminUser], auth=JWTAuth())
    def delete_post(self, post_id: int):
        try:
            self.posts_service.delete(post_id)
        except Post.DoesNotExist:
            return self.create_response(
                {"detail": f"Post not found | id: {post_id}"}, status_code=status.HTTP_404_NOT_FOUND
            )
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("comments", tags=["comments"])
class CommentsController(ControllerBase):
    @http_get("post/{int:post_id}", response=NinjaPaginationResponseSchema[CommentOutSchema])
    @paginate()
    def list_comments_of_post(self, request, post_id: int):
        return get_object_or_404(Post, id=post_id).comment_set.all()

    @http_get("", response=NinjaPaginationResponseSchema[CommentOutSchema])
    @paginate()
    def list_comments(self, request):
        return Comment.objects.all()

    @http_get("{int:comment_id}", response=CommentOutSchema)
    def get_comment(self, request, comment_id: int):
        return get_object_or_404(Comment, id=comment_id)

    @http_post(response=CommentOutSchema)
    def create_comment(self, data: CommentCreateSchema):
        return Comment.objects.create(**data.dict())

    @http_put("{int:comment_id}", response=CommentOutSchema)
    def update_comment(self, comment_id: int, data: CommentUpdateSchema):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_data_dict = data.dict()
        for key, value in comment_data_dict.items():
            setattr(comment, key, value)
        comment.save()
        return comment

    @http_delete("{int:comment_id}")
    def delete_comment(self, comment_id: int):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("replies", tags=["replies"])
class RepliesController(ControllerBase):
    @http_get("comment/{int:comment_id}", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_replies_of_comment(self, request, comment_id: int):
        return get_object_or_404(Comment, id=comment_id).replies.all()

    @http_get("", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_replies(self, request):
        return Reply.objects.all()

    @http_get("{int:reply_id}", response=ReplyOutSchema)
    def get_reply(self, request, reply_id: int):
        return get_object_or_404(Reply, id=reply_id)

    @http_post(response=ReplyOutSchema)
    def create_reply(self, data: ReplyCreateSchema):
        return Reply.objects.create(**data.dict())

    @http_put("{int:reply_id}", response=ReplyOutSchema)
    def update_reply(self, reply_id: int, data: ReplyUpdateSchema):
        reply = get_object_or_404(Reply, id=reply_id)
        reply_data_dict = data.dict()
        for key, value in reply_data_dict.items():
            setattr(reply, key, value)
        reply.save()
        return reply

    @http_delete("{int:reply_id}")
    def delete_reply(self, reply_id: int):
        reply = get_object_or_404(Reply, id=reply_id)
        reply.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)

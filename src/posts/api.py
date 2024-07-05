from django.shortcuts import get_object_or_404
from ninja_extra import ControllerBase, api_controller, http_delete, http_get, http_post, http_put, paginate, status
from ninja_extra.exceptions import NotFound
from ninja_extra.permissions.common import IsAdminUser
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth

from api.schemas import DetailSchema
from posts.exceptions import (
    ContentContainsProfanityAPIError,
    ContentContainsProfanityError,
    EntityDoesNotExistError,
    InvalidRequestBodyError,
    InvalidTitleLengthError,
    RelatedObjectDoesNotExistAPIError,
)
from posts.models import Comment, Post, Reply
from posts.permissions import IsAuthor
from posts.schemas.comments import CommentCreateSchema, CommentOutSchema, CommentUpdateSchema
from posts.schemas.posts import PostCreateSchema, PostOutSchema, PostUpdateSchema
from posts.schemas.replies import ReplyCreateSchema, ReplyOutSchema, ReplyUpdateSchema
from posts.services.comments import AbstractCommentsService
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
        except Post.DoesNotExist as e:
            raise NotFound() from e

    @http_post(
        response={
            200: PostOutSchema,
            201: PostOutSchema,
        },
        auth=JWTAuth(),
    )
    def create_post(self, data: PostCreateSchema):
        try:
            return self.posts_service.create(data)
        except InvalidTitleLengthError as e:
            InvalidRequestBodyError(detail=e.message)
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except EntityDoesNotExistError as e:
            raise RelatedObjectDoesNotExistAPIError(entity_name=e.entity_name, entity_id=e.entity_id) from e

    @http_put(
        "{int:post_id}",
        response={
            200: PostOutSchema,
        },
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def update_post(self, post_id: int, data: PostUpdateSchema):
        try:
            self.posts_service.update(post_id, data)
        except InvalidTitleLengthError as e:
            raise InvalidRequestBodyError(detail=e.message) from e
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except Post.DoesNotExist as e:
            raise NotFound() from e
        post = Post.objects.get(id=post_id)
        return post

    @http_delete("{int:post_id}", permissions=[IsAuthor | IsAdminUser], auth=JWTAuth())
    def delete_post(self, post_id: int):
        try:
            self.posts_service.delete(post_id)
        except Post.DoesNotExist as e:
            raise NotFound() from e
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("comments", tags=["comments"])
class CommentsController(ControllerBase):

    def __init__(self, comments_service: AbstractCommentsService):
        self.comments_service = comments_service

    @http_get(
        "post/{int:post_id}",
        response={
            200: NinjaPaginationResponseSchema[CommentOutSchema],
            404: DetailSchema,
        },
    )
    @paginate()
    def list_comments_of_post(self, request, post_id: int):
        try:
            return self.comments_service.list_by_post(post_id)
        except Post.DoesNotExist as e:
            raise NotFound() from e

    @http_get("", response=NinjaPaginationResponseSchema[CommentOutSchema])
    @paginate()
    def list_comments(self, request):
        return self.comments_service.list()

    @http_get("{int:comment_id}", response=CommentOutSchema)
    def get_comment(self, request, comment_id: int):
        try:
            return self.comments_service.get(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_post(
        response={
            200: CommentOutSchema,
            201: CommentOutSchema,
        },
        auth=JWTAuth(),
    )
    def create_comment(self, data: CommentCreateSchema):
        try:
            return self.comments_service.create(data)
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except EntityDoesNotExistError as e:
            raise RelatedObjectDoesNotExistAPIError(entity_name=e.entity_name, entity_id=e.entity_id) from e

    @http_put(
        "{int:comment_id}",
        response={
            200: CommentOutSchema,
        },
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def update_comment(self, comment_id: int, data: CommentUpdateSchema):
        try:
            self.comments_service.update(comment_id, data)
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except Comment.DoesNotExist as e:
            raise NotFound() from e
        comment = Comment.objects.get(id=comment_id)
        return comment

    @http_delete(
        "{int:comment_id}",
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def delete_comment(self, comment_id: int):
        try:
            self.comments_service.delete(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e
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

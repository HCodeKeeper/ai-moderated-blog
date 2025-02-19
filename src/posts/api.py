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
from posts.services.replies import AbstractRepliesService


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

    @http_get("active", response=NinjaPaginationResponseSchema[PostOutSchema])
    @paginate()
    def list_active_posts(self, request):
        """
        List all active posts

        """
        return self.posts_service.list_active()

    @http_get("{int:post_id}", response=PostOutSchema)
    def get_post(self, request, post_id: int):
        try:
            return self.posts_service.get(post_id)
        except Post.DoesNotExist as e:
            raise NotFound() from e

    @http_get("blocked/{int:post_id}", response=PostOutSchema)
    def get_blocked_post(self, request, post_id: int):
        try:
            return self.posts_service.get_inactive(post_id)
        except Post.DoesNotExist as e:
            raise NotFound() from e

    @http_post(
        response={
            200: PostOutSchema,
            201: PostOutSchema,
        },
        auth=JWTAuth(),
    )
    def create_post(self, request, data: PostCreateSchema):
        try:
            return self.posts_service.create(request.user.id, data)
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

    @http_get("active", response=NinjaPaginationResponseSchema[CommentOutSchema])
    @paginate()
    def list_active_comments(self, request):
        return self.comments_service.list_active()

    @http_get("blocked/post/{int:post_id}", response=CommentOutSchema)
    @paginate()
    def list_blocked_of_post_comments(self, request, post_id: int):
        return self.comments_service.list_inactive_by_post(post_id)

    @http_get("active/post/{int:post_id}", response=CommentOutSchema)
    @paginate()
    def list_active_of_post_comments(self, request, post_id: int):
        return self.comments_service.list_active_by_post(post_id)

    @http_get("{int:comment_id}", response=CommentOutSchema)
    def get_comment(self, request, comment_id: int):
        try:
            return self.comments_service.get(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_get("blocked/{int:comment_id}", response=CommentOutSchema)
    def get_blocked_comment(self, request, comment_id: int):
        try:
            return self.comments_service.get_inactive(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_post(
        response={
            200: CommentOutSchema,
            201: CommentOutSchema,
        },
        auth=JWTAuth(),
    )
    def create_comment(self, request, data: CommentCreateSchema):
        try:
            return self.comments_service.create(request.user.id, data)
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
    def __init__(self, replies_service: AbstractRepliesService):
        self.replies_service = replies_service

    @http_get(
        "comment/{int:comment_id}",
        response={
            200: NinjaPaginationResponseSchema[ReplyOutSchema],
            404: DetailSchema,
        },
    )
    @paginate()
    def list_replies_of_comment(self, request, comment_id: int):
        try:
            return self.replies_service.list_by_comment(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_get("", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_replies(self, request):
        return self.replies_service.list()

    @http_get("active", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_active_replies(self, request):
        return self.replies_service.list_active()

    @http_get("blocked/comment/{int:comment_id}", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_blocked_of_comment_replies(self, request, comment_id: int):
        try:
            return self.replies_service.list_inactive_by_comment(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_get("active/comment/{int:comment_id}", response=NinjaPaginationResponseSchema[ReplyOutSchema])
    @paginate()
    def list_active_of_comment_replies(self, request, comment_id: int):
        try:
            return self.replies_service.list_active_by_comment(comment_id)
        except Comment.DoesNotExist as e:
            raise NotFound() from e

    @http_get("{int:reply_id}", response=ReplyOutSchema)
    def get_reply(self, request, reply_id: int):
        try:
            return self.replies_service.get(reply_id)
        except Reply.DoesNotExist as e:
            raise NotFound() from e

    @http_get("blocked/{int:reply_id}", response=ReplyOutSchema)
    def get_blocked_reply(self, request, reply_id: int):
        try:
            return self.replies_service.get_inactive(reply_id)
        except Reply.DoesNotExist as e:
            raise NotFound() from e

    @http_post(
        response={
            200: ReplyOutSchema,
            201: ReplyOutSchema,
        },
        auth=JWTAuth(),
    )
    def create_reply(self, request, data: ReplyCreateSchema):
        try:
            return self.replies_service.create(request.user.id, data)
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except EntityDoesNotExistError as e:
            raise RelatedObjectDoesNotExistAPIError(entity_name=e.entity_name, entity_id=e.entity_id) from e

    @http_put(
        "{int:reply_id}",
        response={
            200: ReplyOutSchema,
        },
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def update_reply(self, reply_id: int, data: ReplyUpdateSchema):
        try:
            self.replies_service.update(reply_id, data)
        except ContentContainsProfanityError as e:
            raise ContentContainsProfanityAPIError() from e
        except Reply.DoesNotExist as e:
            raise NotFound() from e
        reply = Reply.objects.get(id=reply_id)
        return reply

    @http_delete(
        "{int:reply_id}",
        permissions=[IsAuthor | IsAdminUser],
        auth=JWTAuth(),
    )
    def delete_reply(self, reply_id: int):
        try:
            self.replies_service.delete(reply_id)
        except Reply.DoesNotExist as e:
            raise NotFound() from e
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)

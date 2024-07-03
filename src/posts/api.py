from ninja_extra import ControllerBase, api_controller, http_get, paginate
from ninja_extra.schemas import NinjaPaginationResponseSchema

from posts.models import Post
from posts.schemas import PostOutSchema


@api_controller("posts", tags=["posts"])
class PostsController(ControllerBase):
    @http_get(path="active", response=NinjaPaginationResponseSchema[PostOutSchema])
    @paginate()
    def list_active_posts(self, request):
        """
        List all not blocked posts

        """
        return Post.objects.all().filter(is_blocked=False)

    @http_get(response=NinjaPaginationResponseSchema[PostOutSchema])
    @paginate()
    def list_posts(self, request):
        """
        List all not blocked posts

        """
        return Post.objects.all()

    @http_get("{int:post_id}", response=PostOutSchema)
    def get_post(self, request, post_id: int):
        return Post.objects.get(id=post_id)

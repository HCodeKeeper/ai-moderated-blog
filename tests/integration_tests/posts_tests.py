import pytest

from posts.exceptions import ContentContainsProfanityError, EntityDoesNotExistError
from posts.models import AutoReplyConfig
from posts.schemas.posts import AutoReplyConfigSchemaCreate, PostCreateSchema, PostUpdateSchema
from posts.services.posts import PostsService


@pytest.mark.djano_db
def test_create_post_with_profanity_in_content(user):
    # Arrange
    service = PostsService()
    schema = PostCreateSchema(
        title="Profanity",
        content="This is a post with profanity. Fuck you are so dumb. shit",
        author_id=user.id,
    )

    # Act
    with pytest.raises(ContentContainsProfanityError):
        blocked_post = service.create(schema)
        assert blocked_post is not None
        assert blocked_post.is_blocked is True


@pytest.mark.django_db
def test_create_post_with_profanity_in_title(user):
    service = PostsService()
    schema = PostCreateSchema(
        title="How I fucking hate docker, everything runs perfectly but not the entrypoint.",
        content="Probably will stick to copying the whole dir with tests, what can I do",
        author_id=user.id,
    )

    with pytest.raises(ContentContainsProfanityError):
        blocked_post = service.create(schema)

        assert blocked_post is not None
        assert blocked_post.is_blocked is True


@pytest.mark.django_db
def test_create_post(user):
    service = PostsService()
    title = "AI-moderated blog"
    text = "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support"
    schema = PostCreateSchema(title=title, content=text, author_id=user.id)

    post = service.create(schema)
    assert post.is_blocked is False
    assert post.title == title
    assert post.content == text


@pytest.mark.djano_db
def test_create_post_with_auto_reply(user):
    service = PostsService()
    title = "AI-moderated blog"
    text = "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support"
    schema = PostCreateSchema(
        title=title, content=text, author_id=user.id, auto_reply_config=AutoReplyConfigSchemaCreate(delay_secs=10)
    )
    post = service.create(schema)
    assert AutoReplyConfig.objects.filter(post_id=post.id, delay_secs=10).exists() is True


@pytest.mark.django_db
def test_create_post_with_invalid_author_excepts():
    service = PostsService()
    title = "AI-moderated blog"
    text = "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support"
    schema = PostCreateSchema(title=title, content=text, author_id=0)

    with pytest.raises(EntityDoesNotExistError):
        service.create(schema)


@pytest.mark.django_db
def test_update_post(user):
    service = PostsService()
    title = "AI-moderated blog"
    text = "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support"
    schema = PostCreateSchema(title=title, content=text, author_id=user.id)

    post = service.create(schema)
    new_title = "AI-moderated blog with AI-generated content"
    new_text = (
        "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support. "
        "I'm so happy that I can now use the gemini api"
    )
    update_schema = PostUpdateSchema(title=new_title, content=new_text)

    service.update(post.id, update_schema)
    post.refresh_from_db()
    assert post.title == new_title
    assert post.content == new_text


@pytest.mark.django_db
def test_update_post_with_profanity_in_title(user):
    service = PostsService()
    title = "AI-moderated blog"
    text = "Unfortunately, had to download a vpn and turn on turkish region to enable gemini api support"
    schema = PostCreateSchema(title=title, content=text, author_id=user.id)

    post = service.create(schema)
    profanity_title = "Stupid shit of stupid shit, fuck"
    schema = PostUpdateSchema(
        title=profanity_title,
        content=text,
    )

    with pytest.raises(ContentContainsProfanityError):
        service.update(post.id, schema)
        post.refresh_from_db()
        assert post.title == title

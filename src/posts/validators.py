from posts.exceptions import ContentContainsProfanityError, InvalidContentLengthError, InvalidTitleLengthError
from posts.models import MAX_COMMENT_LENGTH, MAX_TITLE_LENGTH, MIN_COMMENT_LENGTH, MIN_TITLE_LENGTH
from posts.services.profanity import detect_profanity


def validate_post_title(title: str):
    title_length = len(title)
    if title_length < MIN_TITLE_LENGTH:
        raise InvalidTitleLengthError(length=title_length)
    elif title_length > MAX_TITLE_LENGTH:
        raise InvalidTitleLengthError(length=title_length)
    return title


def validate_profanity(contents: [str]):
    if detect_profanity(contents):
        raise ContentContainsProfanityError()


def validate_comment_length(comment: str):
    comment_length = len(comment)
    if comment_length < MIN_COMMENT_LENGTH:
        raise InvalidContentLengthError(length=comment_length, _max=MAX_COMMENT_LENGTH, _min=MIN_COMMENT_LENGTH)
    elif comment_length > MAX_COMMENT_LENGTH:
        raise InvalidContentLengthError(length=comment_length, _max=MAX_COMMENT_LENGTH, _min=MIN_COMMENT_LENGTH)
    return comment

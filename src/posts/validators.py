from posts.exceptions import ContentContainsProfanityError, InvalidTitleLengthError
from posts.models import MAX_TITLE_LENGTH, MIN_TITLE_LENGTH
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

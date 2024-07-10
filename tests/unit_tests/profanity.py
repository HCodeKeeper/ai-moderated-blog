import pytest

from posts.services.profanity import detect_profanity


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("This is a clean sentence.", False),
        ("This shit's crazy", True),
        ("You are shit", True),
        ("You are stupid", True),
        ("I am scared shitless", False),
        ("I am so fucking scared", True),
        ("You are so bad it makes me sick", True),
    ],
)
def test_detect_profanity(test_input, expected):
    assert detect_profanity([test_input]) is expected

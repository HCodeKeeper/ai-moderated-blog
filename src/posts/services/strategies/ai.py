from abc import ABC, abstractmethod
from logging import getLogger

from google import generativeai as genai
from summarizer import Summarizer

from api.settings.local import GEMINI_RPM, GEMINI_SYSTEM_INSTRUCTION, GEMINI_TPM
from posts.models import MAX_COMMENT_LENGTH
from posts.schemas.comments import CommentOutSchema
from posts.schemas.posts import PostOutSchema

logger = getLogger(__name__)


class AbstractAICommentsLimitationsResolverStrategy(ABC):
    def __init__(self, rpm: int, tpm: int):
        self.rpm = rpm
        self.tpm = tpm

    @abstractmethod
    def resolve_comment_tpm(self, comment: str, post: str) -> list[str]:
        pass

    @abstractmethod
    def resolve_reply(self, reply: str, max_length: int) -> str:
        pass


class SimpleAICommentLimitationsResolverStrategy(AbstractAICommentsLimitationsResolverStrategy):
    """
    Naive strategy that summarizes text with BERT when token/length ai/db model's limitations exceed
    Naively treats reply's tokens as words
    """

    COMMENT_PART_IN_PROMPT = 0.5

    def __init__(self, rpm: int, tpm: int):
        super().__init__(rpm, tpm)
        self.tokens_per_request = int(self.tpm / self.rpm)
        self.tokens_per_comment = int(self.tokens_per_request * self.COMMENT_PART_IN_PROMPT)
        self.tokens_per_post = self.tokens_per_request - self.tokens_per_comment
        self.__summarizer = None

    @property
    def summarizer(self):
        if self.__summarizer is None:
            self.__summarizer = Summarizer()
        return self.__summarizer

    @summarizer.setter
    def summarizer(self, value):
        raise AttributeError("Summarizer cannot be set")

    def resolve_comment_tpm(self, comment: str, post: str) -> list[str]:
        """
        Resolves the comment and post length to fit limitations of tpm/rpm giving precedence to comment
        """
        # Naive tokenization considering that the ai model uses tokens as words
        if len(comment.split()) > self.tokens_per_comment:
            comment = self.summarizer(comment, max_length=self.tokens_per_comment)
        if len(post.split()) > self.tokens_per_post:
            post = self.summarizer(post, max_length=self.tokens_per_post)
        return [comment, post]

    def resolve_reply(self, reply: str, max_length: int) -> str:
        """
        Resolves the reply length to fit the db models limitations
        """

        if len(reply) > max_length:
            reply = self.summarizer(reply, max_length=max_length)

        return reply


class AbstractAIResponseStrategy(ABC):

    @abstractmethod
    def get_personalized_response(self, post: PostOutSchema, comment: CommentOutSchema) -> str:
        pass


class GeminiAIResponseStrategy(AbstractAIResponseStrategy):
    """
    Don't instantiate this class directly, use the gemini_response_strategy var as a singleton
    Response strategy that handles integration with Gemini model and limitations resolution
    """

    # As tokens can be [sub]words, the actual token count can be gradually higher
    MAX_REPLY_TOKENS = 100

    def __init__(
        self,
        limits_resolver: AbstractAICommentsLimitationsResolverStrategy = SimpleAICommentLimitationsResolverStrategy(
            GEMINI_RPM, GEMINI_TPM
        ),
    ):
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=GEMINI_SYSTEM_INSTRUCTION,
            generation_config={"max_output_tokens": self.MAX_REPLY_TOKENS},
        )
        self.limits_resolver = limits_resolver

    def get_personalized_response(self, post: PostOutSchema, comment: CommentOutSchema) -> str:
        # Opting out from resolving until doesnt properly work
        # comment, post = self.limits_resolver.resolve_comment_tpm(comment.content, post.content)
        comment = comment.content
        post = post.content
        prompt = "User commented: " + comment + ". \n| This is the post content: " + post
        logger.info("Sending prompt to Gemini: %s", prompt)
        reply = self.model.generate_content(prompt).text
        reply = self.limits_resolver.resolve_reply(reply, MAX_COMMENT_LENGTH)

        return reply


# Instead of singleton
gemini_response_strategy = GeminiAIResponseStrategy()

"""
===========================================================
ClickDetect AI
Reasoning Layer Exceptions
===========================================================

Custom exceptions used throughout the reasoning engine.

===========================================================
"""


class ReasoningException(Exception):
    """
    Base exception for all reasoning-related errors.
    """

    def __init__(self, message: str):
        super().__init__(message)


class ConfidenceReasonerException(ReasoningException):
    """
    Raised when confidence evaluation fails.
    """

    pass


class HeadlineReasonerException(ReasoningException):
    """
    Raised when headline reasoning fails.
    """

    pass


class YoutubeTextReasonerException(ReasoningException):
    """
    Raised when YouTube text reasoning fails.
    """

    pass


class MetadataReasonerException(ReasoningException):
    """
    Raised when metadata reasoning fails.
    """

    pass


class ImageReasonerException(ReasoningException):
    """
    Raised when image reasoning fails.
    """

    pass


class YoutubeReasonerException(ReasoningException):
    """
    Raised when multimodal reasoning fusion fails.
    """

    pass


class ResponseBuilderException(ReasoningException):
    """
    Raised when API response construction fails.
    """

    pass


class ReasonEngineException(ReasoningException):
    """
    Raised by the main orchestration engine.
    """

    pass
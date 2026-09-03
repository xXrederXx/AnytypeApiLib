
from .lib import AnyApiError


class APIError(AnyApiError):
    """An error returned by the Anytype API."""

    def __init__(self, message: str, status: int):
        super().__init__(f"APIError: {status} {message}")
        self.message = message
        self.status = status


class BadRequestError(APIError):
    """Bad request"""


class UnauthorizedError(APIError):
    """Unauthorized"""


class NotFoundError(APIError):
    """Not found"""


class ForbiddenError(APIError):
    """Forbidden"""


class ResourceDeletedError(APIError):
    """Resource deleted"""


class RateLimitError(APIError):
    """Rate limit exceeded"""


class InternalServerError(APIError):
    """Internal server error"""

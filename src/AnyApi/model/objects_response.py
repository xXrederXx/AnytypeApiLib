from pydantic import Field

from .base import APIResponseModel
from .object import AnyObject
from .space import AnySpace
from .pagination import AnyPagination


class AnyObjectsResponse(APIResponseModel):
    """Paginated response containing a list of Anytype objects."""

    data: list[AnyObject] = Field(
        description="Objects returned by the current request."
    )
    pagination: AnyPagination = Field(
        description="Pagination metadata for the result set."
    )

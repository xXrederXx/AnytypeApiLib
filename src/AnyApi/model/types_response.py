from pydantic import Field

from .base import APIResponseModel
from .type import AnyType
from .pagination import AnyPagination


class AnyTypesResponse(APIResponseModel):
    """Paginated response containing a list of Anytype Types."""

    data: list[AnyType] = Field(description="Types returned by the current request.")
    pagination: AnyPagination = Field(
        description="Pagination metadata for the result set."
    )

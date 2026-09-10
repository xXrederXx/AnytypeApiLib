from pydantic import Field

from .base import APIResponseModel
from .space import AnySpace
from .pagination import AnyPagination


class AnySpacesResponse(APIResponseModel):
    """Paginated response containing a list of Anytype spaces."""

    data: list[AnySpace] = Field(description="Spaces returned by the current request.")
    pagination: AnyPagination = Field(
        description="Pagination metadata for the response."
    )

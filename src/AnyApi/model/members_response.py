from pydantic import Field

from .member import AnyMember
from .base import APIResponseModel
from .pagination import AnyPagination


class AnyMembersResponse(APIResponseModel):
    """Paginated response containing a list of Anytype Members."""

    data: list[AnyMember] = Field(
        description="Members returned by the current request."
    )
    pagination: AnyPagination = Field(
        description="Pagination metadata for the result set."
    )

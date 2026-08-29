
from pydantic import BaseModel, Field


class AnyPagination(BaseModel):
    """Pagination metadata returned by Anytype list endpoints."""

    total: int = Field(description="Total number of items available.")
    offset: int = Field(description="Current offset into the result set.")
    limit: int = Field(description="Maximum number of items requested per page.")
    has_more: bool = Field(description="Whether additional pages of results exist.")
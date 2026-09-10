from pydantic import Field

from .base import APIResponseModel


class AnySelect(APIResponseModel):
    """Selectable option metadata used by property values in Anytype."""

    object: str = Field(description="Object type identifier for the selection.")
    id: str = Field(description="Unique identifier of the option.")
    key: str = Field(description="Storage key for the selection.")
    name: str = Field(description="User-facing label of the option.")
    color: str = Field(description="Color code for the selection option.")

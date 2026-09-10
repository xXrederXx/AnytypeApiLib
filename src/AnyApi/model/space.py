from pydantic import Field

from .base import APIResponseModel
from .icon import AnyIcon


class AnySpace(APIResponseModel):
    """Representation of an Anytype space."""

    object: str = Field(description="Object type identifier for the space.")
    id: str = Field(description="Unique identifier of the space.")
    name: str = Field(description="Display name of the space.")
    icon: AnyIcon | None = Field(
        default=None, description="Icon metadata for the space."
    )
    description: str = Field(description="Human-readable description of the space.")
    gateway_url: str = Field(description="Gateway URL for this space.")
    network_id: str = Field(description="Network identifier associated with the space.")

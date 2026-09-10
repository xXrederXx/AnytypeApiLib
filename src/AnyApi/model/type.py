from pydantic import Field

from .base import APIResponseModel
from .property import AnyProperty
from .icon import AnyIcon


class AnyType(APIResponseModel):
    """Definition of an Anytype object type and its property schema."""

    object: str = Field(description="Object type identifier for this schema.")
    id: str = Field(description="Unique identifier of the type.")
    key: str = Field(description="Internal key used to reference the type.")
    name: str = Field(description="Singular display name of the type.")
    plural_name: str = Field(description="Plural display name of the type.")
    icon: AnyIcon | None = Field(description="Icon metadata associated with the type.")
    archived: bool = Field(description="Whether this type is archived.")
    layout: str = Field(description="Layout template applied to the type.")
    properties: list[AnyProperty] = Field(
        description="Property definitions for this object type."
    )

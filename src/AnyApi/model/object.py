from pydantic import BaseModel, Field

from .property import AnyProperty
from .type import AnyType
from .icon import AnyIcon


class AnyObject(BaseModel):
    """Representation of an Anytype object and its associated properties."""

    archived: bool = Field(description="Whether the object has been archived.")
    id: str = Field(description="Unique identifier of the object.")
    icon: AnyIcon | None = Field(default=None, description="Icon metadata for the object.")
    layout: str = Field(description="Layout type used to render the object.")
    name: str = Field(description="Display name of the object.")
    object: str = Field(description="Object type identifier, usually 'object'.")
    properties: list[AnyProperty] = Field(description="Properties defined for the object.")
    snippet: str = Field(description="Text snippet or summary for the object.")
    space_id: str = Field(description="Identifier of the space containing the object.")
    type: AnyType = Field(description="Type definition associated with the object.")
    markdown: str | None = Field(default=None, description="Optional markdown content for the object.")

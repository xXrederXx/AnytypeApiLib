from pydantic import Field

from .base import APIResponseModel
from .property import AnyProperty
from .type import AnyType
from .icon import AnyIcon


class AnyObject(APIResponseModel):
    """Representation of an Anytype object and its associated properties."""

    archived: bool = Field(description="Whether the object has been archived.")
    id: str = Field(description="Unique identifier of the object.")
    icon: AnyIcon | None = Field(
        default=None, description="Icon metadata for the object."
    )
    layout: str = Field(description="Layout type used to render the object.")
    name: str = Field(description="Display name of the object.")
    object: str = Field(description="Object type identifier, usually 'object'.")
    properties: list[AnyProperty] = Field(
        description="Properties defined for the object."
    )
    snippet: str = Field(description="Text snippet or summary for the object.")
    space_id: str = Field(description="Identifier of the space containing the object.")
    type: AnyType = Field(description="Type definition associated with the object.")
    markdown: str | None = Field(
        default=None, description="Optional markdown content for the object."
    )

    def get_prop_by_name(self, name) -> AnyProperty:
        """
        Retrieve a property by its name.

        Args:
            name: The name of the property to find.

        Returns:
            The AnyProperty object matching the given name.

        Raises:
            ValueError: If no property with the given name exists on this object.
        """
        for prop in self.properties:
            if prop.name == name:
                return prop
        raise ValueError(
            f"Could not find property with name {name} on obj {self.name} [{self.id}]"
        )

    def get_prop_by_id(self, prop_id) -> AnyProperty:
        """
        Retrieve a property by its ID.

        Args:
            prop_id: The ID of the property to find.

        Returns:
            The AnyProperty object matching the given ID.

        Raises:
            ValueError: If no property with the given ID exists on this object.
        """
        for prop in self.properties:
            if prop.id == prop_id:
                return prop
        raise ValueError(
            f"Could not find property with id {prop_id} on obj {self.name} [{self.id}]"
        )

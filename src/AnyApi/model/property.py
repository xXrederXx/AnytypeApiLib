
from datetime import datetime

from pydantic import BaseModel, Field

from .select import AnySelect


class AnyProperty(BaseModel):
    """Schema for an Anytype object property, including its value and formatting."""

    object: str = Field(description="Type of the object this property belongs to.")
    id: str = Field(description="Unique identifier of the property.")
    key: str = Field(description="Property key used in the Anytype schema.")
    name: str = Field(description="Human-readable name of the property.")
    format: str = Field(description="Data format for the property value.")
    objects: list[str] | None = Field(default=None, description="List of related object identifiers when applicable.")
    select: AnySelect | None = Field(default=None, description="Single selected option for the property.")
    date: datetime | None = Field(default=None, description="Date value when the property is a date.")
    multi_select: list[AnySelect] | None = Field(default=None, description="Multiple selected options when the property supports them.")
    text: str | None = Field(default=None, description="Text value when the property stores plain text.")
    url: str | None = Field(default=None, description="URL value when the property stores a URL.")
    number: int | float | None = Field(default=None, description="Numeric value when the property stores a number.")

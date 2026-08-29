from pydantic import BaseModel, Field


class AnyIcon(BaseModel):
    """Metadata describing an object icon, including its visual style and label."""

    format: str = Field(description="Icon format identifier used by Anytype.")
    emoji: str | None = Field(default=None, description="Emoji character used for the icon when available.")
    name: str | None = Field(default=None, description="Human-readable icon name.")
    color: str | None = Field(default=None, description="Color associated with the icon.")
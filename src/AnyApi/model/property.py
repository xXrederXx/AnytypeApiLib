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
    objects: list[str] | None = Field(
        default=None, description="List of related object identifiers when applicable."
    )
    select: AnySelect | None = Field(
        default=None, description="Single selected option for the property."
    )
    date: datetime | None = Field(
        default=None, description="Date value when the property is a date."
    )
    multi_select: list[AnySelect] | None = Field(
        default=None,
        description="Multiple selected options when the property supports them.",
    )
    text: str | None = Field(
        default=None, description="Text value when the property stores plain text."
    )
    url: str | None = Field(
        default=None, description="URL value when the property stores a URL."
    )
    number: int | float | None = Field(
        default=None, description="Numeric value when the property stores a number."
    )

    def get_objects(self, default: list[str] | None = None) -> list[str]:
        """
        Retrieve the list of related object identifiers.
        
        Args:
            default: Optional default value to return if objects is None.
        
        Returns:
            The list of related object identifiers.
        
        Raises:
            ValueError: If objects is None and no default value is provided.
        """
        if self.objects:
            return self.objects
        if default:
            return default
        raise ValueError(
            f"Invalid access, objects is None. Property Format is {self.format}"
        )

    def get_select(self, default: AnySelect | None = None) -> AnySelect:
        """
        Retrieve the single selected option for the property.
        
        Args:
            default: Optional default value to return if select is None.
        
        Returns:
            The selected AnySelect option.
        
        Raises:
            ValueError: If select is None and no default value is provided.
        """
        if self.select:
            return self.select
        if default:
            return default
        raise ValueError(
            f"Invalid access, select is None. Property Format is {self.format}"
        )

    def get_date(self, default: datetime | None = None) -> datetime:
        """
        Retrieve the date value of the property.
        
        Args:
            default: Optional default value to return if date is None.
        
        Returns:
            The date value.
        
        Raises:
            ValueError: If date is None and no default value is provided.
        """
        if self.date:
            return self.date
        if default:
            return default
        raise ValueError(
            f"Invalid access, date is None. Property Format is {self.format}"
        )

    def get_multi_select(
        self, default: list[AnySelect] | None = None
    ) -> list[AnySelect]:
        """
        Retrieve the list of multiple selected options.
        
        Args:
            default: Optional default value to return if multi_select is None.
        
        Returns:
            The list of selected AnySelect options.
        
        Raises:
            ValueError: If multi_select is None and no default value is provided.
        """
        if self.multi_select:
            return self.multi_select
        if default:
            return default
        raise ValueError(
            f"Invalid access, multi_select is None. Property Format is {self.format}"
        )

    def get_text(self, default: str | None = None) -> str:
        """
        Retrieve the text value of the property.
        
        Args:
            default: Optional default value to return if text is None.
        
        Returns:
            The text value.
        
        Raises:
            ValueError: If text is None and no default value is provided.
        """
        if self.text:
            return self.text
        if default:
            return default
        raise ValueError(
            f"Invalid access, text is None. Property Format is {self.format}"
        )

    def get_url(self, default: str | None = None) -> str:
        """
        Retrieve the URL value of the property.
        
        Args:
            default: Optional default value to return if url is None.
        
        Returns:
            The URL value.
        
        Raises:
            ValueError: If url is None and no default value is provided.
        """
        if self.url:
            return self.url
        if default:
            return default
        raise ValueError(
            f"Invalid access, url is None. Property Format is {self.format}"
        )

    def get_number(self, default: int | float | None = None) -> int | float:
        """
        Retrieve the numeric value of the property.
        
        Args:
            default: Optional default value to return if number is None.
        
        Returns:
            The numeric value.
        
        Raises:
            ValueError: If number is None and no default value is provided.
        """
        if self.number:
            return self.number
        if default:
            return default
        raise ValueError(
            f"Invalid access, number is None. Property Format is {self.format}"
        )

from pydantic import BaseModel, ConfigDict


class APIResponseModel(BaseModel):
    """Base class for all API Models. Includes only pydantic configuration"""

    model_config = ConfigDict(
        extra="forbid",  # Reject fields returned by the API that aren't in the model
        strict=False,  # Allow normal Pydantic type coercion for JSON values
        validate_assignment=False,  # Response objects aren't expected to be mutated
        validate_default=False,  # Defaults don't need extra validation
        frozen=True,  # Don't allow consumers to modify response objects
        populate_by_name=False,  # Don't accept field names when an alias is defined
        use_enum_values=False,  # Keep Enum instances rather than converting to their values
        from_attributes=False,  # Responses come from JSON/dicts, not ORM objects
        arbitrary_types_allowed=False,  # Require fields to use Pydantic-supported types
        revalidate_instances="never",  # Don't revalidate already-validated Pydantic models
        validate_by_alias=True,  # Accept API aliases when validating input
        validate_by_name=False,  # Don't additionally accept Python field names
        serialize_by_alias=False,  # Serialize using Python field names by default
        loc_by_alias=True,  # Validation errors refer to API field names
    )

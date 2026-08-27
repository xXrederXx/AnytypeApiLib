from pydantic import BaseModel

from .property import AnyProperty
from .type import AnyType
from .icon import AnyIcon


class AnyObject(BaseModel):
    archived: bool
    id: str
    icon: AnyIcon | None
    layout: str
    name: str
    object: str
    properties: list[AnyProperty]
    snippet: str
    space_id: str
    type: AnyType
    markdown: str | None = None

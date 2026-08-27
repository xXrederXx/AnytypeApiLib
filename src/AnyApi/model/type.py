from pydantic import BaseModel

from .icon import AnyIcon

class AnyType(BaseModel):
    object: str
    id: str
    key: str
    name: str
    plural_name: str
    icon: AnyIcon
    archived: bool
    layout: str
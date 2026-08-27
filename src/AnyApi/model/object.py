from pydantic import BaseModel

from .icon import AnyIcon

class AnyObject(BaseModel):
    archived: bool
    id: str
    icon: AnyIcon
    layout: any
    name: str
    object: str
    properties: any
    snippet: str
    space_id: str
    type: any
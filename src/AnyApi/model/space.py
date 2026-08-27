from pydantic import BaseModel

from .icon import AnyIcon

class AnySpace(BaseModel):
    object: str
    id: str
    name: str
    icon: AnyIcon | None
    description: str
    gateway_url: str
    network_id: str
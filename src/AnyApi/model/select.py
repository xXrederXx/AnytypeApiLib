from pydantic import BaseModel


class AnySelect(BaseModel):
    object: str
    id: str
    key: str
    name: str
    color: str

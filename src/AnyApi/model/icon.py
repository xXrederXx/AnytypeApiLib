from pydantic import BaseModel

class AnyIcon(BaseModel):
    format: str
    emoji: str | None = None
    name: str | None = None
    color: str | None = None
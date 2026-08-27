from pydantic import BaseModel

class AnyIcon(BaseModel):
    format: str
    emoji: str
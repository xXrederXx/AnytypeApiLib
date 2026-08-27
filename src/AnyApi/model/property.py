
from datetime import datetime

from pydantic import BaseModel

from .select import AnySelect


class AnyProperty(BaseModel):
    object: str
    id: str
    key: str
    name: str
    format: str
    objects: list[str] | None = None
    select: AnySelect | None = None
    date: datetime | None = None
    multi_select: list[AnySelect] | None = None
    text: str | None = None
    url: str | None = None
    number: int | float | None = None

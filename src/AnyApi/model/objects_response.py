from pydantic import BaseModel

from .object import AnyObject
from .space import AnySpace
from .pagination import AnyPagination


class AnyObjectsResponse(BaseModel):
    data: list[AnyObject]
    pagination: AnyPagination

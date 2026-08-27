from pydantic import BaseModel

from .space import AnySpace
from .pagination import AnyPagination

class AnySpacesResponse(BaseModel):
    data: list[AnySpace]
    pagination: AnyPagination
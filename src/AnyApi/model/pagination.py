
from pydantic import BaseModel

class AnyPagination(BaseModel):
    total: int
    offset: int
    limit: int
    has_more: bool
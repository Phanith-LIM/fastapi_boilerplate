from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field



class CreateBook(BaseModel):
    title: str
    description: str


class ResponseBookAddedBy(BaseModel):
    id: int
    username: str
    created_at: datetime

class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    author: ResponseBookAddedBy = Field(..., alias='added_by')


class BookUpdate(CreateBook):
    pass

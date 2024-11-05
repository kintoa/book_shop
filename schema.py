from pydantic import BaseModel
from typing import Optional, List

class BookSchema(BaseModel):
    name: str
    author_id: int

class BookPutUpdateSchema(BookSchema):
    id: int

class BookPatchUpdateScema(BaseModel):
    id: int
    name: Optional[str] = None
    author: Optional[int] = None

class BookDeleteSchema(BaseModel):
    id: int


class AuthorSchema(BaseModel):
    name: str

class AuthorBooksSchema(AuthorSchema):
    books: List[BookSchema]

class AuthorFullSchema(AuthorSchema):
    id: int
from .router import router
from db import database
from models import Book
from schema import BookSchema, BookPutUpdateSchema, BookPatchUpdateScema, BookDeleteSchema

@router.get("/book/", tags=["books"], response_model=list[BookSchema])
async def get_books():
    # Эндпоинт получения всех книг
    response = await database.get_all(Book)
    return response

@router.post("/book/", tags=["books"], response_model=BookSchema)
async def create_book(book: BookSchema):
    # Эндпоинт создания книг
    response = await database.add(Book, name=book.name, author_id=book.author_id)
    return response

@router.put("/book/", tags=["books"], response_model=BookSchema)
async def update_all_fields(book: BookPutUpdateSchema):
    # Эндпоинт полного обновления книги
    response = await database.update(Book, book.id, name=book.name, author_id=book.author_id)
    return response

@router.patch("/book/", tags=["books"], response_model=BookSchema)
async def update_book(book: BookPatchUpdateScema):
    #Эндпоинт частичного обновления книги
    update_fields = {}
    for field in book.model_fields_set:
        value = getattr(book, field, None)
        if value is not None and field != "id":
            update_fields[field] = value
    response = await database.update(Book, book.id, **update_fields)
    return response

@router.delete("/book/", tags=["books"], response_model=BookSchema)
async def delete_book(book: BookDeleteSchema):
    # Эндпоинт удаления книги
    response = await database.delete(Book, book.id)
    return response
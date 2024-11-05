from .router import router
from db import database, author
from models import Author
from schema import AuthorSchema, AuthorBooksSchema, AuthorFullSchema
from connection_manager import manager
from fastapi import WebSocket, WebSocketDisconnect
import json

@router.get("/author/", tags=["authors"], response_model=list[AuthorSchema])
async def get_authors():
    # Эндпоинт получения всех авторов
    response = await database.get_all(Author)

    return response if response is not None else []

@router.post("/author/", tags=["authors"], response_model=AuthorSchema)
async def create_author(author: AuthorSchema):
    # Эндпоинт создания автора
    response = await database.add(Author, name=author.name)
    authors = await database.get_all(Author)
    authors_json = [
            AuthorFullSchema(name = author.name, id = author.id).model_dump() for author in authors
           ]
    await manager.notify_all(authors_json)
    return response

@router.get("/author/books", tags=["authors"], response_model=list[AuthorBooksSchema])
async def get_authors_books():
    # Эндпоинт получения списка авторов с их книгами начинающиемся на M
    response = await author.get_author_books_like_m()

    return response

@router.websocket("/ws/authors")
async def websocket_authors(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Отправляем текущий список авторов при подключении
        authors = await database.get_all(Author)
        authors_json = [
            AuthorFullSchema(name = author.name, id = author.id).model_dump() for author in authors
           ]
        await websocket.send_json(authors_json)
        while True:
            data = await websocket.receive_text()
            author_data = json.loads(data)
            if author_name := author_data.get("name"):
                await database.add(Author, name=author_name)

            # Получаем обновленный список авторов
                authors = await database.get_all(Author)
                authors_json = [
                    AuthorFullSchema(name=author.name, id=author.id).model_dump() for author in authors
                ]
                await manager.notify_all(authors_json)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
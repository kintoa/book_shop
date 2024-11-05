from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
import os
from sqlalchemy import func

Base = declarative_base()

class DB:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=True)
        self.Session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init_db(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def add(self, model, **kwargs):
        async with self.Session() as session:
            new_record = model(**kwargs)
            session.add(new_record)
            await session.commit()
        return new_record

    async def get_all(self, model):
        async with self.Session() as session:
            result = await session.execute(select(model))
            records = result.scalars().all()
        return records

    async def update(self, model, update_id, **kwargs):
        async with self.Session() as session:
            result = await session.execute(select(model).where(model.id == update_id))
            record = result.scalar_one_or_none()
            if record:
                for key, value in kwargs.items():
                    setattr(record, key, value)
                await session.commit()
        return record

    async def delete(self, model, delete_id):
        async with self.Session() as session:
            result = await session.execute(select(model).where(model.id == delete_id))
            deleting_record = result.scalar_one_or_none()
            if deleting_record:
                await session.delete(deleting_record)
                await session.commit()
        return deleting_record

class Author(DB):
    def __init__(self, db_url):
        super().__init__(db_url)

    async def get_author_books_like_m(self):
        from models import Author, Book
        async with self.Session() as session:
            result = await session.execute(
                select(Author).join(Author.books).options(contains_eager(Author.books)).filter(func.lower(Book.name).like("m%"))
            )
            authors = result.unique().scalars().all()
        return authors

database = DB(os.getenv("DATABASE_URL"))
author = Author(os.getenv("DATABASE_URL"))
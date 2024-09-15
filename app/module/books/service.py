from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.module.books.entity import BookEntity
from app.module.books.model import CreateBook, BookUpdate
from app.module.users.entity import UserEntity


class BookService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_books(self):
        return self.db.query(BookEntity).options(joinedload(BookEntity.added_by)).all()

    def create_book(self, book: CreateBook, user: UserEntity):
        new_book = BookEntity(**book.model_dump())
        new_book.author_id = user.id
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def get_book(self, book_id: int):
        book = self.db.query(BookEntity).filter(BookEntity.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Item not found")
        return book

    def delete_book(self, book_id: int):
        book = self.get_book(book_id)
        self.db.delete(book)
        self.db.commit()
        return book

    def update_book(self, book_id: int, book_update: BookUpdate):
        book: BookEntity = self.get_book(book_id)
        book.title = book_update.title
        book.description = book_update.description
        self.db.commit()
        self.db.refresh(book)
        return book

    def set_author(self, user_id: int):
        all_books = self.db.query(BookEntity).filter(BookEntity.author_id == user_id).all()
        for book in all_books:
            book.author_id = None
        self.db.commit()
        self.db.refresh(all_books)
        return all_books

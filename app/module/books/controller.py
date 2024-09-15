from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException, status

from app.core.guards.authentication import AuthGuard
from app.core.guards.authorization import AuthorizeGuard
from app.module.books.model import CreateBook, BookUpdate, BookResponse
from app.module.books.service import BookService
from app.module.users.entity import UserEntity
from app.utils.common.user_role import UserRoles

router = APIRouter(
    prefix="/book",
    tags=["Books"],
)

@router.get('', response_model=List[BookResponse], dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN]))])
def get_books(book_service: BookService = Depends(BookService)):
    return book_service.get_books()

@router.post('', dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN, UserRoles.USER]))])
def create_book(req: Request, book: CreateBook, book_service: BookService = Depends(BookService)):
    user: UserEntity = req.state.current_user
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return book_service.create_book(book, user)

@router.get("/{id}", dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN, UserRoles.USER]))])
def get_book(id: int, book_service: BookService = Depends(BookService)):
    return book_service.get_book(id)

@router.put("/{id}", dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN, UserRoles.USER]))])
def update_book(id: int, book: BookUpdate, book_service: BookService = Depends(BookService)):
    return book_service.update_book(id, book)

@router.delete("/{id}", dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN]))])
def delete_book(id: int, book_service: BookService = Depends(BookService)):
    return book_service.delete_book(id)

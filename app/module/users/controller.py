from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.core.guards.authentication import AuthGuard
from app.core.guards.authorization import AuthorizeGuard
from app.module.users.entity import UserEntity
from app.module.users.model import ResponseUser, UpdateUser, LoginUser, TokenModel, SignUpUser
from app.module.users.service import UserService
from app.utils.common.user_role import UserRoles

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get('', response_model=List[ResponseUser], dependencies=[Depends(AuthGuard()), Depends(AuthorizeGuard([UserRoles.ADMIN]))])
def get_users(user_service: UserService = Depends(UserService)) -> List[ResponseUser]:
    return user_service.get_users()

@router.post("/admin", response_model=ResponseUser)
def create_admin(user_service: UserService = Depends(UserService)):
    return user_service.create_admin()


@router.get("/me", dependencies=[Depends(AuthGuard())], response_model=ResponseUser)
def read_user(req: Request):
    user: UserEntity = req.state.current_user
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


@router.put("/{id}", response_model=ResponseUser, dependencies=[Depends(AuthGuard())])
def update(id: int, user: UpdateUser, user_service: UserService = Depends(UserService)):
    return user_service.update_user(id, user)


@router.delete("/{id}", response_model=ResponseUser, dependencies=[Depends(AuthGuard())])
def delete(id: int, user_service: UserService = Depends(UserService)):
    return user_service.delete_user(id)


@router.post("/sign-up", response_model=ResponseUser)
def create_user(user: SignUpUser, user_service: UserService = Depends(UserService)):
    return user_service.create_user(user)


@router.post("/login", response_model=TokenModel)
def login(user: LoginUser, user_service: UserService = Depends(UserService)):
    return user_service.login_user(user)

from typing import List
from fastapi import status, HTTPException, Request

from app.module.users.entity import UserEntity
from app.utils.common.user_role import UserRoles


class AuthorizeGuard:
    def __init__(self, allowed_roles: List[UserRoles]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request):
        user: UserEntity = request.state.current_user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_roles = getattr(user, "roles", [])
        try:
            user_roles_enum = [UserRoles(role) for role in user_roles]
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        if not user_roles_enum or not any(role in self.allowed_roles for role in user_roles_enum):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        return user
#
# class AuthorizeGuard:
#     def __init__(self, allowed_roles: List[UserRoles]):
#         self.allowed_roles = allowed_roles
#
#     async def __call__(self, request: Request):
#         user = request.state.current_user
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#         if not user.roles or not any(role in self.allowed_roles for role in user.roles):
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#         return user

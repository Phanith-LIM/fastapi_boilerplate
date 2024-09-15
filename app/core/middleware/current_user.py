from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.module.users.entity import UserEntity
from app.module.users.service import UserService
from app.core.database import SessionLocal
import jwt
import os


class CurrentUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService(db=SessionLocal())

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            request.state.current_user = None
        else:
            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(
                    token,
                    key=os.getenv('SECRET_KEY'),
                    algorithms=[os.getenv('ALGORITHM')]
                )
                user_id = int(payload.get("sub"))
                user: UserEntity = self.user_service.get_user(user_id)
                if user:
                    request.state.current_user = user
                else:
                    request.state.current_user = None
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
                request.state.current_user = None

        response = await call_next(request)
        return response

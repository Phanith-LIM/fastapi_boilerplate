from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

class AuthGuard(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthGuard, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AuthGuard, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication schema.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            return True
        except jwt.PyJWTError:
            return False

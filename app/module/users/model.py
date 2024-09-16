from datetime import datetime
from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str

class ResponseUser(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    roles: list


class SignUpUser(CreateUser):
    pass

class CreateAdmin(CreateUser):
    roles: list

class UpdateUser(CreateUser):
    pass

class LoginUser(CreateUser):
    pass

class TokenModel(BaseModel):
    access_token: str
    type: str
    user: ResponseUser

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.users.entity import UserEntity
from app.module.users.model import CreateUser, UpdateUser, LoginUser, TokenModel, ResponseUser, SignUpUser

load_dotenv()

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db: Session = db

    def get_users(self):
        return self.db.query(UserEntity).all()

    def create_user(self, user: SignUpUser):
        new_user = UserEntity(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user(self, user_id: int):
        user: UserEntity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        print(user.roles)
        if not user:
            raise HTTPException(status_code=404, detail="Item not found")
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
        return user

    def update_user(self, user_id: int, user_update: UpdateUser):
        user: UserEntity = self.get_user(user_id)
        user.username = user_update.username
        user.password = user_update.password
        self.db.commit()
        self.db.refresh(user)
        return user

    def login_user(self, user: LoginUser):
        is_match: UserEntity = self.db.query(UserEntity).filter(user.username == UserEntity.username).first()
        if not is_match:
            raise HTTPException(status_code=404, detail="username not found")
        if user.password is is_match.password:
            raise HTTPException(status_code=401, detail="Password is incorrect")
        payload = {
            "sub": is_match.id,
            "username": is_match.username,
        }
        return TokenModel(
            access_token=self.generate_token(payload),
            type='Bearer',
            user=ResponseUser(
                id=is_match.id,
                username=is_match.username,
                created_at=is_match.created_at,
                updated_at=is_match.updated_at,
                roles=is_match.roles
            )
        )

    @staticmethod
    def generate_token(payload: dict, expires_in_minutes: int = 30):
        payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        payload["iat"] = datetime.now(timezone.utc)
        payload["jti"] = os.urandom(16).hex()

        return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

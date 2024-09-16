from sqlalchemy import Column, String, DateTime, Integer, ARRAY
from datetime import datetime, timezone
from sqlalchemy.orm import deferred, relationship
from app.core.database import Base
from app.utils.common.user_role import UserRoles


class UserEntity(Base):
    __tablename__ = 'users'
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = deferred(Column(String, nullable=False))
    roles = Column(ARRAY(String), default=lambda: [UserRoles.USER.value])
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    books = relationship("BookEntity", back_populates='added_by')

    def __repr__(self):
        return f"<UserEntity(id={self.id}, username={self.username})>"

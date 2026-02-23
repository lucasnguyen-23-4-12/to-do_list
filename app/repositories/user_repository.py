from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserORM
from app.schemas.user import UserCreate


def get_by_email(db: Session, email: str) -> Optional[UserORM]:
    stmt = select(UserORM).where(UserORM.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_by_id(db: Session, user_id: int) -> Optional[UserORM]:
    return db.get(UserORM, user_id)


def create_user(db: Session, data: UserCreate, hashed_password: str) -> UserORM:
    user = UserORM(
        email=data.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
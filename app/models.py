from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from .db import Base, utcnow


class TodoORM(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at = Column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )
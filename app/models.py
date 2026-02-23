from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .db import Base, utcnow


# Association table for many-to-many relationship between Todo and Tag
todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    todos = relationship("TodoORM", back_populates="owner")


class TodoORM(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True, index=True)

    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("UserORM", back_populates="todos")
    tags = relationship("TagORM", secondary=todo_tags, back_populates="todos")


class TagORM(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    
    todos = relationship("TodoORM", secondary=todo_tags, back_populates="tags")
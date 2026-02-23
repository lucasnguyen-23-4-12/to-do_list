from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class TagRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    # dùng cho POST /todos
    tags: Optional[List[str]] = None  # danh sách tên tag


class TodoUpdate(TodoBase):
    # dùng cho PUT /todos/{id} (update full)
    tags: Optional[List[str]] = None


class TodoUpdatePartial(BaseModel):
    # dùng cho PATCH /todos/{id} (update 1 phần)
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []

    class Config:
        from_attributes = True
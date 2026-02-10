from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False


class TodoCreate(TodoBase):
    # dùng cho POST /todos
    pass


class TodoUpdate(TodoBase):
    # dùng cho PUT /todos/{id} (update full)
    pass


class TodoUpdatePartial(BaseModel):
    # dùng cho PATCH /todos/{id} (update 1 phần)
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
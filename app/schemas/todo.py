from pydantic import BaseModel, Field
from datetime import datetime

class Todo(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

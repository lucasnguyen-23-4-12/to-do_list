from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.todo import Todo
from app.services import todo_service

router = APIRouter(prefix="/api/v1/todos", tags=["Todos"])


@router.post("/", status_code=201)
def create(todo: Todo):
    return todo_service.create_todo(todo)


@router.get("/")
def get_all(
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    return todo_service.get_todos(is_done, q, sort, limit, offset)


@router.get("/{todo_id}")
def get_one(todo_id: int):
    return todo_service.get_todo(todo_id)


@router.put("/{todo_id}")
def update(todo_id: int, updated: Todo):
    return todo_service.update_todo(todo_id, updated)


@router.delete("/{todo_id}")
def delete(todo_id: int):
    return todo_service.delete_todo(todo_id)

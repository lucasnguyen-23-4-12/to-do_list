from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import todo_repository
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoUpdatePartial,
    TodoRead,
)


def create_todo(db: Session, data: TodoCreate) -> TodoRead:
    # nếu bạn muốn check trùng title, v.v. thì làm ở đây
    todo = todo_repository.create(db, data=data)
    return TodoRead.from_orm(todo)


def get_todos(
    db: Session,
    *,
    is_done: Optional[bool],
    q: Optional[str],
    sort: Optional[str],
    limit: int,
    offset: int,
):
    items = todo_repository.get_all(
        db,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    total = todo_repository.count_all(
        db,
        is_done=is_done,
        q=q,
    )

    return {
        "items": [TodoRead.from_orm(t) for t in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_todo(db: Session, todo_id: int) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoRead.from_orm(todo)


def update_todo(db: Session, todo_id: int, data: TodoUpdate) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.update(db, todo=todo, data=data)
    return TodoRead.from_orm(todo)


def patch_todo(db: Session, todo_id: int, data: TodoUpdatePartial) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.partial_update(db, todo=todo, data=data)
    return TodoRead.from_orm(todo)


def complete_todo(db: Session, todo_id: int) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.mark_complete(db, todo=todo)
    return TodoRead.from_orm(todo)


def delete_todo(db: Session, todo_id: int):
    todo = todo_repository.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo_repository.delete(db, todo=todo)
    return {"detail": "Deleted"}
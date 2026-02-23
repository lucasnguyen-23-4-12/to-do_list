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
from app.models import UserORM


def create_todo(db: Session, data: TodoCreate, current_user: UserORM) -> TodoRead:
    # nếu bạn muốn check trùng title, v.v. thì làm ở đây
    todo = todo_repository.create(db, data=data, owner_id=current_user.id)
    return TodoRead.from_orm(todo)


def get_todos(
    db: Session,
    *,
    current_user: UserORM,
    is_done: Optional[bool],
    q: Optional[str],
    sort: Optional[str],
    limit: int,
    offset: int,
):
    items = todo_repository.get_all(
        db,
        owner_id=current_user.id,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    total = todo_repository.count_all(
        db,
        owner_id=current_user.id,
        is_done=is_done,
        q=q,
    )

    return {
        "items": [TodoRead.from_orm(t) for t in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_overdue_todos(
    db: Session,
    current_user: UserORM,
    limit: int,
    offset: int,
):
    """Lấy danh sách todo quá hạn"""
    items = todo_repository.get_overdue(
        db,
        owner_id=current_user.id,
        limit=limit,
        offset=offset,
    )
    total = todo_repository.count_overdue(db, owner_id=current_user.id)

    return {
        "items": [TodoRead.from_orm(t) for t in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_today_todos(
    db: Session,
    current_user: UserORM,
    limit: int,
    offset: int,
):
    """Lấy danh sách todo hôm nay"""
    items = todo_repository.get_today(
        db,
        owner_id=current_user.id,
        limit=limit,
        offset=offset,
    )
    total = todo_repository.count_today(db, owner_id=current_user.id)

    return {
        "items": [TodoRead.from_orm(t) for t in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_todo(db: Session, todo_id: int, current_user: UserORM) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoRead.from_orm(todo)


def update_todo(db: Session, todo_id: int, data: TodoUpdate, current_user: UserORM) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.update(db, todo=todo, data=data)
    return TodoRead.from_orm(todo)


def patch_todo(db: Session, todo_id: int, data: TodoUpdatePartial, current_user: UserORM) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.partial_update(db, todo=todo, data=data)
    return TodoRead.from_orm(todo)


def complete_todo(db: Session, todo_id: int, current_user: UserORM) -> TodoRead:
    todo = todo_repository.get_by_id(db, todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = todo_repository.mark_complete(db, todo=todo)
    return TodoRead.from_orm(todo)


def delete_todo(db: Session, todo_id: int, current_user: UserORM):
    todo = todo_repository.get_by_id(db, todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo_repository.delete(db, todo=todo)
    return {"detail": "Deleted"}
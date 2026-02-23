from typing import Optional, List

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoUpdatePartial,
    TodoRead,
)
from app.services import todo_service
from app.deps import get_current_user
from app.models import UserORM

router = APIRouter(prefix="/api/v1/todos", tags=["Todos"])


@router.post("/", status_code=201, response_model=TodoRead)
def create(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.create_todo(db, todo, current_user)


@router.get("/", response_model=dict)
def get_all(
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.get_todos(
        db,
        current_user=current_user,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@router.get("/overdue", response_model=dict)
def get_overdue(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    """Lấy danh sách todo quá hạn (is_done=False và due_date < hôm nay)"""
    return todo_service.get_overdue_todos(db, current_user, limit, offset)


@router.get("/today", response_model=dict)
def get_today(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    """Lấy danh sách todo hôm nay (is_done=False và due_date = hôm nay)"""
    return todo_service.get_today_todos(db, current_user, limit, offset)


@router.get("/{todo_id}", response_model=TodoRead)
def get_one(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.get_todo(db, todo_id, current_user)


@router.put("/{todo_id}", response_model=TodoRead)
def update(
    todo_id: int,
    updated: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.update_todo(db, todo_id, updated, current_user)


@router.patch("/{todo_id}", response_model=TodoRead)
def patch(
    todo_id: int,
    body: TodoUpdatePartial,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.patch_todo(db, todo_id, body, current_user)


@router.post("/{todo_id}/complete", response_model=TodoRead)
def complete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.complete_todo(db, todo_id, current_user)


@router.delete("/{todo_id}")
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return todo_service.delete_todo(db, todo_id, current_user)
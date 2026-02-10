from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TodoORM
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoUpdatePartial,
)


def get_all(
    db: Session,
    *,
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> List[TodoORM]:
    query = select(TodoORM)

    # filter is_done
    if is_done is not None:
        query = query.where(TodoORM.is_done == is_done)

    # search q trong title
    if q:
        like = f"%{q}%"
        query = query.where(TodoORM.title.ilike(like))

    # sort
    if sort:
        desc = sort.startswith("-")
        field = sort.lstrip("-")

        if field == "created_at":
            col = TodoORM.created_at
        elif field == "title":
            col = TodoORM.title
        else:
            col = TodoORM.id

        if desc:
            col = col.desc()

        query = query.order_by(col)

    # pagination thực từ DB
    query = query.offset(offset).limit(limit)

    return db.execute(query).scalars().all()

def count_all(
    db: Session,
    *,
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
) -> int:
    query = select(TodoORM)

    if is_done is not None:
        query = query.where(TodoORM.is_done == is_done)

    if q:
        like = f"%{q}%"
        query = query.where(TodoORM.title.ilike(like))

    # Lấy hết rồi dùng len(...) để đếm
    return len(db.execute(query).scalars().all())


def get_by_id(db: Session, todo_id: int) -> Optional[TodoORM]:
    return db.get(TodoORM, todo_id)


def create(db: Session, data: TodoCreate) -> TodoORM:
    todo = TodoORM(
        title=data.title,
        description=data.description,
        is_done=data.is_done,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update(db: Session, todo: TodoORM, data: TodoUpdate) -> TodoORM:
    todo.title = data.title
    todo.description = data.description
    todo.is_done = data.is_done
    db.commit()
    db.refresh(todo)
    return todo


def partial_update(
    db: Session,
    todo: TodoORM,
    data: TodoUpdatePartial,
) -> TodoORM:
    # chỉ update field được gửi lên
    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.is_done is not None:
        todo.is_done = data.is_done

    db.commit()
    db.refresh(todo)
    return todo


def mark_complete(db: Session, todo: TodoORM) -> TodoORM:
    todo.is_done = True
    db.commit()
    db.refresh(todo)
    return todo


def delete(db: Session, todo: TodoORM) -> None:
    db.delete(todo)
    db.commit()
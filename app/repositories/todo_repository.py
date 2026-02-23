from typing import List, Optional
from datetime import datetime, date

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import TodoORM, TagORM
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoUpdatePartial,
)


def get_all(
    db: Session,
    *,
    owner_id: int,
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> List[TodoORM]:
    # chỉ lấy todo của user này
    query = select(TodoORM).where(TodoORM.owner_id == owner_id)

    if is_done is not None:
        query = query.where(TodoORM.is_done == is_done)

    if q:
        like = f"%{q}%"
        query = query.where(TodoORM.title.ilike(like))

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

    query = query.offset(offset).limit(limit)
    return db.execute(query).scalars().all()
def count_all(
    db: Session,
    *,
    owner_id: int,
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
) -> int:
    query = select(TodoORM).where(TodoORM.owner_id == owner_id)

    if is_done is not None:
        query = query.where(TodoORM.is_done == is_done)

    if q:
        like = f"%{q}%"
        query = query.where(TodoORM.title.ilike(like))

    return len(db.execute(query).scalars().all())

def get_by_id(db: Session, todo_id: int, owner_id: int) -> Optional[TodoORM]:
    stmt = select(TodoORM).where(
        TodoORM.id == todo_id,
        TodoORM.owner_id == owner_id,
    )
    return db.execute(stmt).scalar_one_or_none()

def create(db: Session, data: TodoCreate, owner_id: int) -> TodoORM:
    todo = TodoORM(
        title=data.title,
        description=data.description,
        is_done=data.is_done,
        due_date=data.due_date,
        owner_id=owner_id,
    )
    db.add(todo)
    db.flush()  # flush to get the ID
    
    # Add tags nếu có
    if data.tags:
        for tag_name in data.tags:
            stmt = select(TagORM).where(TagORM.name == tag_name)
            tag = db.execute(stmt).scalar_one_or_none()
            if not tag:
                tag = TagORM(name=tag_name)
                db.add(tag)
                db.flush()
            todo.tags.append(tag)
    
    db.commit()
    db.refresh(todo)
    return todo


def update(db: Session, todo: TodoORM, data: TodoUpdate) -> TodoORM:
    todo.title = data.title
    todo.description = data.description
    todo.is_done = data.is_done
    todo.due_date = data.due_date
    
    # Update tags
    if data.tags is not None:
        todo.tags.clear()
        for tag_name in data.tags:
            stmt = select(TagORM).where(TagORM.name == tag_name)
            tag = db.execute(stmt).scalar_one_or_none()
            if not tag:
                tag = TagORM(name=tag_name)
                db.add(tag)
                db.flush()
            todo.tags.append(tag)
    
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
    if data.due_date is not None:
        todo.due_date = data.due_date
    
    # Update tags
    if data.tags is not None:
        todo.tags.clear()
        for tag_name in data.tags:
            stmt = select(TagORM).where(TagORM.name == tag_name)
            tag = db.execute(stmt).scalar_one_or_none()
            if not tag:
                tag = TagORM(name=tag_name)
                db.add(tag)
                db.flush()
            todo.tags.append(tag)

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


def get_overdue(
    db: Session,
    owner_id: int,
    limit: int = 10,
    offset: int = 0,
) -> List[TodoORM]:
    """Get todo quá hạn (due_date < hôm nay và is_done = False)"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    query = select(TodoORM).where(
        and_(
            TodoORM.owner_id == owner_id,
            TodoORM.is_done == False,
            TodoORM.due_date < today,
        )
    ).order_by(TodoORM.due_date.asc())
    
    query = query.offset(offset).limit(limit)
    return db.execute(query).scalars().all()


def count_overdue(db: Session, owner_id: int) -> int:
    """Đếm số todo quá hạn"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    query = select(TodoORM).where(
        and_(
            TodoORM.owner_id == owner_id,
            TodoORM.is_done == False,
            TodoORM.due_date < today,
        )
    )
    return len(db.execute(query).scalars().all())


def get_today(
    db: Session,
    owner_id: int,
    limit: int = 10,
    offset: int = 0,
) -> List[TodoORM]:
    """Get todo hôm nay (due_date = hôm nay và is_done = False)"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = datetime.fromtimestamp(today.timestamp() + 86400)
    
    query = select(TodoORM).where(
        and_(
            TodoORM.owner_id == owner_id,
            TodoORM.is_done == False,
            TodoORM.due_date >= today,
            TodoORM.due_date < tomorrow,
        )
    ).order_by(TodoORM.due_date.asc())
    
    query = query.offset(offset).limit(limit)
    return db.execute(query).scalars().all()


def count_today(db: Session, owner_id: int) -> int:
    """Đếm số todo hôm nay"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = datetime.fromtimestamp(today.timestamp() + 86400)
    
    query = select(TodoORM).where(
        and_(
            TodoORM.owner_id == owner_id,
            TodoORM.is_done == False,
            TodoORM.due_date >= today,
            TodoORM.due_date < tomorrow,
        )
    )
    return len(db.execute(query).scalars().all())
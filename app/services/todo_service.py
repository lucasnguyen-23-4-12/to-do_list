from fastapi import HTTPException
from typing import Optional
from app.schemas.todo import Todo
from app.repositories import todo_repository
import json
import time


# region agent log
def _agent_log(run_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    try:
        ts = int(time.time() * 1000)
        payload = {
            "id": f"log_{ts}",
            "timestamp": ts,
            "location": location,
            "message": message,
            "data": data,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
        }
        with open(
            r"c:\Users\Admin\Documents\PROJECT_IT\to-do_list\.cursor\debug.log",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        # tránh làm hỏng luồng chính nếu log lỗi
        pass


# endregion


def create_todo(todo: Todo):
    existing = todo_repository.get_by_id(todo.id)
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")

    # region agent log
    _agent_log(
        run_id="pre-fix",
        hypothesis_id="H1",
        location="app/services/todo_service.py:create_todo",
        message="create_todo called",
        data={"todo_id": todo.id},
    )
    # endregion

    return todo_repository.create(todo)


def get_todos(
    is_done: Optional[bool],
    q: Optional[str],
    sort: Optional[str],
    limit: int,
    offset: int,
):
    results = todo_repository.get_all().copy()

    # region agent log
    _agent_log(
        run_id="pre-fix",
        hypothesis_id="H2",
        location="app/services/todo_service.py:get_todos",
        message="get_todos initial",
        data={
            "count": len(results),
            "is_done": is_done,
            "q": q,
            "sort": sort,
            "limit": limit,
            "offset": offset,
        },
    )
    # endregion

    # filter
    if is_done is not None:
        results = [t for t in results if t.is_done == is_done]

    # search
    if q:
        results = [t for t in results if q.lower() in t.title.lower()]

    # sort
    if sort:
        reverse = sort.startswith("-")
        field_name = sort.lstrip("-")

        if field_name == "created_at":
            results.sort(key=lambda x: x.created_at, reverse=reverse)

    total = len(results)
    results = results[offset: offset + limit]

    # region agent log
    _agent_log(
        run_id="pre-fix",
        hypothesis_id="H3",
        location="app/services/todo_service.py:get_todos",
        message="get_todos final",
        data={"returned": len(results), "total": total},
    )
    # endregion

    return {
        "items": results,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_todo(todo_id: int):
    todo = todo_repository.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def update_todo(todo_id: int, updated: Todo):
    existing = todo_repository.get_by_id(todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated.created_at = existing.created_at
    return todo_repository.update(todo_id, updated)


def delete_todo(todo_id: int):
    deleted = todo_repository.delete(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted

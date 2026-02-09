from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# =========================
# Model dữ liệu
# =========================
class Todo(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


# "Database giả"
todos: List[Todo] = []


# =========================
# POST /todos
# =========================
@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    for existing in todos:
        if existing.id == todo.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    todos.append(todo)
    return todo


# =========================
# GET /todos
# Filter + Search + Sort + Pagination
# =========================
@app.get("/todos")
def get_todos(
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    results = todos.copy()

    # 1️⃣ Filter
    if is_done is not None:
        results = [todo for todo in results if todo.is_done == is_done]

    # 2️⃣ Search
    if q:
        results = [todo for todo in results if q.lower() in todo.title.lower()]

    # 3️⃣ Sort
    if sort:
        reverse = sort.startswith("-")
        field_name = sort.lstrip("-")

        if field_name == "created_at":
            results.sort(key=lambda x: x.created_at, reverse=reverse)

    total = len(results)

    # 4️⃣ Pagination
    results = results[offset: offset + limit]

    return {
        "items": results,
        "total": total,
        "limit": limit,
        "offset": offset
    }


# =========================
# GET /todos/{id}
# =========================
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")


# =========================
# PUT /todos/{id}
# =========================
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            updated_todo.created_at = todo.created_at
            todos[index] = updated_todo
            return updated_todo

    raise HTTPException(status_code=404, detail="Todo not found")


# =========================
# DELETE /todos/{id}
# =========================
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(index)

    raise HTTPException(status_code=404, detail="Todo not found")

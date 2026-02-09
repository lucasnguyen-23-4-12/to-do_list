from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# =========================
# Model dữ liệu
# =========================
class Todo(BaseModel):
    id: int
    title: str
    is_done: bool = False

# "Database giả" trong RAM
todos: List[Todo] = []

# =========================
# 1️⃣ POST /todos - Tạo todo
# =========================
# @app.post("/todos", status_code=201)
# def create_todo(todo: Todo):
#     # kiểm tra id đã tồn tại chưa
#     for existing in todos:
#         if existing.id == todo.id:
#             raise HTTPException(status_code=400, detail="ID already exists")

#     todos.append(todo)
#     return todo

# =========================
# POST nhiều todo cùng lúc
# =========================
@app.post("/todos", status_code=201)
def create_todos(todo_list: List[Todo]):
    for todo in todo_list:
        # kiểm tra id trùng
        for existing in todos:
            if existing.id == todo.id:
                raise HTTPException(status_code=400, detail=f"ID {todo.id} already exists")

        todos.append(todo)

    return todo_list
# =========================
# 2️⃣ GET /todos - Lấy danh sách
# =========================
@app.get("/todos")
def get_todos():
    return todos


# =========================
# 3️⃣ GET /todos/{id} - Lấy chi tiết
# =========================
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")


# =========================
# 4️⃣ PUT /todos/{id} - Cập nhật toàn bộ
# =========================
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo

    raise HTTPException(status_code=404, detail="Todo not found")


# =========================
# 5️⃣ DELETE /todos/{id} - Xóa
# =========================
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int):
#     for index, todo in enumerate(todos):
#         if todo.id == todo_id:
#             deleted = todos.pop(index)
#             return deleted

#     raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos")
def delete_multiple_todos(ids: List[int]):
    deleted_items = []
    not_found_ids = []

    for todo_id in ids:
        found = False
        for index, todo in enumerate(todos):
            if todo.id == todo_id:
                deleted_items.append(todos.pop(index))
                found = True
                break

        if not found:
            not_found_ids.append(todo_id)

    return {
        "deleted": deleted_items,
        "not_found": not_found_ids
    }
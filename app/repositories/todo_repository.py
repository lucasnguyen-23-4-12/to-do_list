from typing import List
from app.schemas.todo import Todo

# database giả
todos: List[Todo] = []

def get_all():
    return todos

def get_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None

def create(todo: Todo):
    todos.append(todo)
    return todo

def update(todo_id: int, updated: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated
            return updated
    return None

def delete(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(index)
    return None

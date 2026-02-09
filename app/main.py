from fastapi import FastAPI
from app.routers.todo import router as todo_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(todo_router)

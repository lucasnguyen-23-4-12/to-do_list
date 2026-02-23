from fastapi import FastAPI

from app.core.config import settings
from app.routers import auth, todo

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(auth.router)
app.include_router(todo.router)

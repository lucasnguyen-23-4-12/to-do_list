from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate, UserRead, Token
from app.repositories import user_repository
from app.deps import get_current_user
from app.models import UserORM

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    existing = user_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(data.password)
    user = user_repository.create_user(db, data, hashed_password=hashed)
    return UserRead.from_orm(user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_repository.get_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: UserORM = Depends(get_current_user)):
    return UserRead.from_orm(current_user)
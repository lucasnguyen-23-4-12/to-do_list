from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import get_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_access_token(token)
    except JWTError:
        raise credentials_exception

    if token_data.user_id is None:
        raise credentials_exception

    user = get_by_id(db, token_data.user_id)
    if not user or not user.is_active:
        raise credentials_exception

    return user
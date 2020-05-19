import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app.users import crud as user_crud
from app.api.utils.db import get_db, get_async_db
import config
from app.core.jwt import ALGORITHM
from app.users.controller import User
from app.utils.models.token import TokenPayload
from databases import Database

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/chat/login/access-token")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Security(reusable_oauth2),
    async_db: Database = Depends(get_async_db),
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await user_crud.get(async_db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

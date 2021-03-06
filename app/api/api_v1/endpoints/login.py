from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.users import crud as user_crud
from app.api.utils.db import get_db, get_async_db
from app.api.utils.security import get_current_user
import config
from app.core.jwt import create_access_token
from app.core.security import get_password_hash
from app.users.model import User as UserORM
from app.utils.controller import Msg
from app.utils.models.token import Token
from app.users.controller import User
from app.utils.controller import verify_password_reset_token
from databases import Database

router = APIRouter()


@router.post("/login/access-token", response_model=Token, tags=["login"])
async def login_access_token(
    async_db: Database = Depends(get_async_db),
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        async_db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_crud.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["login"], response_model=User)
async def test_token(current_user: UserORM = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


# @router.post("/reset-password/", tags=["login"], response_model=Msg)
# def reset_password(
#     token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)
# ):
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = user_crud.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not user_crud.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}

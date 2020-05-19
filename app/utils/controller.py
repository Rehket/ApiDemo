from typing import Optional
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError

import config

password_reset_jwt_subject = "preset"


class Msg(BaseModel):
    msg: str


def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None

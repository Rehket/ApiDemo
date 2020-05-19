from typing import Optional, List, Dict, Union
import io
import csv

import jwt
from jwt.exceptions import InvalidTokenError

import config

password_reset_jwt_subject = "preset"


def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None


def dict_to_csv(
    data: List[Dict[str, Union[str, int, float]]],
    header: List[str],
    restval: str = "",
    extrasaction: str = "ignore",
    quoting: int = csv.QUOTE_MINIMAL,
):
    csv_buffer = io.StringIO(newline="\n")
    writer = csv.DictWriter(
        csv_buffer, header, restval=restval, extrasaction=extrasaction, quoting=quoting
    )

    writer.writerows(data)

    csv_buffer.seek(0)

    return csv_buffer

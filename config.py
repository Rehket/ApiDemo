from os import getenv, urandom, supports_bytes_environ
import tempfile
from pathlib import Path
import ssl


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/chat"

if supports_bytes_environ:
    from os import getenvb
    SECRET_KEY = getenvb(b"SECRET_KEY")
else:
    SECRET_KEY = getenv("SECRET_KEY").encode()

if not SECRET_KEY:
    SECRET_KEY = urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SERVER_HOST = getenv("SERVER_HOST")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION", False)

PROJECT_NAME = getenv("PROJECT_NAME")

FIRST_SUPERUSER = getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = getenv("FIRST_SUPERUSER_PASSWORD")

POSTGRES_SERVER = getenv("POSTGRES_SERVER")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_PORT = getenv("POSTGRES_PORT")
POSTGRES_SCHEMA = getenv("POSTGRES_SCHEMA")
API_QUERY_LIMIT = getenv("API_QUERY_LIMIT")
RDS_CERTIFICATE_PATH = getenv("RDS_CERTIFICATE_PATH")
LOCAL_DEV = getenv_boolean("LOCAL_DEV", False)
PUBLIC_TABLES = []

# LOCAL_DEV is used to indicate a local database, DOCKER
RDS_SSL_CONTEXT = (
    ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, cafile=RDS_CERTIFICATE_PATH
    )
    if not LOCAL_DEV
    else None
)

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?options=-csearch_path={POSTGRES_SCHEMA}"

BACKEND_CORS_ORIGINS = getenv(
    "BACKEND_CORS_ORIGINS",
    "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8000",
)

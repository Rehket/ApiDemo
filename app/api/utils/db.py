from starlette.requests import Request


def get_db(request: Request):
    return request.state.a_db


def get_async_db(request: Request):
    return request.state.a_db

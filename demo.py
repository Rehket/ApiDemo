from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Message(BaseModel):
    message: str


class Item(BaseModel):
    id: int
    name: str


item_db = [
    Item(id=1, name="Socks"),
    Item(id=2, name="Gloves"),
    Item(id=3, name="Shoes"),
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items", response_model=List[Item], responses={500: {"model": Message}})
def read_items():
    """
    Return a list of all items in the database.
    """
    return item_db


@app.get(
    "/items/{item_id}",
    responses={200: {"model": Item}, 404: {"model": Message}, 500: {"model": Message}},
)  # /items/3
def read_item(item_id: int):
    """
    This retrieves an item specified by the item_id.
    """

    items = [item for item in item_db if item.id == item_id]
    if len(items) == 0:
        return JSONResponse(
            status_code=404,
            content=Message(
                message="The item you have requested is not available."
            ).dict(),
        )
    return items[0]


@app.post("/items")
def create_item():
    pass

from fastapi import FastAPI
from pydantic import BaseModel

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


@app.get("/items/{item_id}")
def read_item(item_id: int):
    items = [item for item in item_db if item.id == item_id]
    return items[0]

@app.post("/items")
def create_item():
    pass
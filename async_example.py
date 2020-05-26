
from pydantic import BaseModel
import time
from datetime import datetime, timedelta

import asyncio

class Item(BaseModel):
    id: int
    name: str

class ItemDatabase:
    """
    A class to act like a rudimentry database.
    """
    item_db = [
        Item(id=1, name="Socks"),
        Item(id=2, name="Gloves"),
        Item(id=3, name="Shoes"),
    ]
    
    def fetch(self, item_id: int):
        """
        Example of a dummy database call that takes some time to execute.
        """
        items = [item for item in self.item_db if item.id == item_id]
        time.sleep(2)
        if len(items) == 0:
            raise KeyError(f"Item with Id: {item_id} not present in the database.")
        return items[0]
    
    async def async_fetch(self, item_id: int):
        """
        Example of a dummy database call that takes some time to execute using async syntax.
        """
        items = [item for item in self.item_db if item.id == item_id]
        await asyncio.sleep(2)
        if len(items) == 0:
            raise KeyError(f"Item with Id: {item_id} not present in the database.")
        return items[0]

my_database = ItemDatabase()


def sync_db_example(item_id: int) -> Item:
    """
    Retrieves a value from the database and prints how long it took to retrieve the data.
    """
    start_time = datetime.now()
    item = my_database.fetch(item_id)
    print(f"Retrieved {item}, finish Time: {datetime.now() - start_time}, {datetime.now()}")
    return item


def run_the_sync_code():
    """
    Wrapper to run all the Sync code with timing. 
    """
    start_time = datetime.now()
    sync_db_example(1)
    sync_db_example(3)
    print(f"Finished retrieving all items, finish Time: {datetime.now() - start_time}, {datetime.now()}")


async def async_db_example(item_id: int):
    """
    Retrieves values from the database asynchronously.
    """
    start_time = datetime.now()
    item = await my_database.async_fetch(item_id)
    print(f"Retrieved {item}, finish Time: {datetime.now() - start_time}, {datetime.now()}")
    return item

async def run_the_async_code():
    start_time = datetime.now()
    await async_db_example(1)
    await async_db_example(3)
    print(f"Finished retrieving all items, finish Time: {datetime.now() - start_time}, {datetime.now()}")

async def hello_world():
    await asyncio.sleep(3)
    return "Hello  World"

async def with_gather():
    start_time = datetime.now()

    my_results = await asyncio.gather(
        async_db_example(1),
        async_db_example(3),
        hello_world()
    )
    print(f"Finished retrieving all items, finish Time: {datetime.now() - start_time}, {datetime.now()}")

    print(my_results)

if __name__ == "__main__":
    # sync_db_example(2)

    asyncio.run(with_gather())
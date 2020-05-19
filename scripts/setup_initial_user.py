# Used to bootstrap a dev environment.

import config
from time import time
from datetime import timedelta
import asyncio
from databases import Database


async def setup_initial_users(async_db: Database):
    from app.users.crud import get_by_email
    from app.core.security import get_password_hash

    user = await get_by_email(async_db=async_db, email=config.FIRST_SUPERUSER)
    if not user:
        await async_db.execute(
            query=f"INSERT INTO {config.POSTGRES_SCHEMA}.user(email, hashed_password, is_active, is_superuser) VALUES (:email, :hashed_password, :is_active, :is_superuser)",
            values={
                "email": config.FIRST_SUPERUSER,
                "hashed_password": get_password_hash(config.FIRST_SUPERUSER_PASSWORD),
                "is_active": True,
                "is_superuser": True,
            },
        )


async def setup_user():

    async with Database(
        config.DATABASE_URI, ssl=config.RDS_SSL_CONTEXT
    ) as database:
        await setup_initial_users(database)


if __name__ == "__main__":

    start_time = time()
    asyncio.run(setup_user())

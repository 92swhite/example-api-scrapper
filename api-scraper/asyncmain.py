import os
import asyncio
import aiohttp
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import create_async_engine
from helpers.async_api_handler import ApiHandler  # type: ignore


async def main(engine):
    api_handler = ApiHandler()
    await api_handler.async_init()
    new_releases_list = api_handler.get_new_releases()
    async for new_releases in new_releases_list:

        exit()


if __name__ == "__main__":
    conn_string = (
        "postgresql+asyncpg://"
        f"{os.environ['DB_USERNAME']}:"
        f"{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_SERVER']}:"
        f"5432/"
        f"{os.environ['DB_DATABASE']}"
    )
    engine = create_async_engine(conn_string)
    asyncio.run(main(engine))
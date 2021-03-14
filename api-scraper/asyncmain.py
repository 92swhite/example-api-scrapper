import os
import time
import asyncio
import logging
from collections import Counter
from helpers.async_api_handler import ApiHandler  # type: ignore
from helpers.async_db_handler import DbHandler  # type: ignore


async def main():
    counter = Counter()
    start_time = time.time()
    api_handler = ApiHandler()
    await api_handler.async_init()
    logging.info("API SUCCESSFULL")
    db_handler = DbHandler()
    await db_handler.reset_tables()
    logging.info("DB SUCCESSFUL")
    new_releases_list = api_handler.get_new_releases()
    async for new_releases in new_releases_list:
        logging.info(f"UPSERTING {len(new_releases)} RECORDS")
        await db_handler.handle_new_releases(new_releases, counter)
        logging.info("\tGREAT SUCCESS!")


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    logging.basicConfig(level=logging_level)
    asyncio.run(main())

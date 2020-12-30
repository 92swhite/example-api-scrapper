import os
import logging
from helpers.api_handler import ApiHandler
from helpers.db_handler import DbHandler


def main():
    # api_handler = ApiHandler(testing=True)
    # new_releases = api_handler.get_new_releases()
    db_handler = DbHandler()


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    logging.basicConfig(level=logging_level)
    main()
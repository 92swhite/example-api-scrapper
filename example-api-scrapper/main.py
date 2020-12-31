import os
import logging
from helpers.api_handler import ApiHandler
from helpers.db_handler import DbHandler


def main(testing: bool):
    api_handler = ApiHandler(testing)
    db_handler = DbHandler()
    for new_releases in api_handler.get_new_releases():
        db_handler.handle_new_releases(new_releases)


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    testing = os.getenv("TESTING", False)
    logging.basicConfig(level=logging_level)
    main(testing)
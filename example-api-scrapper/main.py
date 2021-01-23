import os
import logging
import argparse
from typing import Dict
from helpers.api_handler import ApiHandler  # type: ignore
from helpers.db_handler import DbHandler  # type: ignore


def main(testing: bool):
    api_handler = ApiHandler(testing)
    db_handler = DbHandler()
    for new_releases in api_handler.get_new_releases():
        db_handler.handle_new_releases(new_releases)


def __get_args() -> Dict[str, bool]:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("-t", "--testing", action="store_true", default=False)
    return vars(parser.parse_args())


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    logging.basicConfig(level=logging_level)
    args = __get_args()
    main(args["testing"])
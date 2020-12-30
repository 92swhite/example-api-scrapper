import os
import logging
from helpers.api_handler import ApiHandler


def main():
    api_handler = ApiHandler(testing=True)
    stuff = api_handler.get_new_releases()
    print(stuff)


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    logging.basicConfig(level=logging_level)
    main()
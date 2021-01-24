import os
import logging
import argparse
from typing import Dict, Counter as CounterType
from collections import Counter
from helpers.api_handler import ApiHandler  # type: ignore
from helpers.db_handler import DbHandler  # type: ignore


def main(testing: bool):
    api_handler = ApiHandler(testing)
    db_handler = DbHandler()
    counter = Counter()
    for new_releases in api_handler.get_new_releases():
        db_handler.handle_new_releases(new_releases, counter)
    __logging_stats(counter)


def __get_args() -> Dict[str, bool]:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("-t", "--testing", action="store_true", default=False)
    return vars(parser.parse_args())


def __logging_stats(counter: CounterType) -> None:
    display_len = 40
    symbols = ("\n\t" + ("=" * display_len)) * 2
    wrapped_title = __get_wrapped_text(display_len, f"Upsertes", " ")
    wrapped_artists = __get_wrapped_text(display_len, f"Artists: {counter['artists']}")
    wrapped_albums = __get_wrapped_text(display_len, f"Albums: {counter['albums']}")
    display_message = f"""
    {symbols}
    {wrapped_title}
    {wrapped_artists}
    {wrapped_albums}
    {symbols}
    """
    logging.info(display_message)


def __get_wrapped_text(display_len: int, text: str, symbol: str = "☆") -> str:
    message_len = display_len - len(text)
    message_symbol = (symbol + " ") * int(message_len / 4)
    return f"\n\t{message_symbol}{text}{message_symbol[::-1]}"


if __name__ == "__main__":
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    logging.basicConfig(level=logging_level)
    args = __get_args()
    main(args["testing"])
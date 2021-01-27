import os
import time
import json
import logging
import argparse
import subprocess
from typing import Dict, Counter as CounterType
from collections import Counter
from helpers.api_handler import ApiHandler  # type: ignore
from helpers.db_handler import DbHandler  # type: ignore


def main_pull(testing: bool) -> None:
    api_handler = ApiHandler(testing)
    db_handler = DbHandler()
    counter = Counter()
    start_time = time.time()
    for new_releases in api_handler.get_new_releases():
        db_handler.handle_new_releases(new_releases, counter)
    __logging_stats(counter, start_time)


def main_kafka() -> None:
    logging.info("POSTING CONSUMER TO KAFKA CONNECT...")
    result = subprocess.run(["../kafka/post.sh"], capture_output=True)
    result_dict = json.loads(result.stdout)
    if "error_code" in result_dict:
        logging.error(f"FAILED TO POST! {result_dict}")
        raise UserWarning("Is the kafka connect cluster up and reciving posts?")
    else:
        logging.info("SUCCESS!")


def __get_args(parser: argparse.ArgumentParser) -> Dict[str, bool]:
    parser.add_argument("-t", "--testing", action="store_true", default=False)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--pull", action="store_const", dest="mode", const="pull")
    mode.add_argument("-k", "--kafka", action="store_const", dest="mode", const="kafka")
    parser.set_defaults(mode="pull")
    return vars(parser.parse_args())


def __logging_stats(counter: CounterType, start_time: float) -> None:
    display_len = 40
    symbols = ("\n\t" + ("=" * display_len)) * 2
    wrapped_title = __get_wrapped_text(display_len, f"Upserts", " ")
    wrapped_artists = __get_wrapped_text(display_len, f"Artists: {counter['artists']}")
    wrapped_albums = __get_wrapped_text(display_len, f"Albums: {counter['albums']}")
    wrapped_time = __get_wrapped_text(
        display_len, f"In {round(time.time() - start_time, 2)} seconds!"
    )
    display_message = f"""
    {symbols}
    {wrapped_title}
    {wrapped_artists}
    {wrapped_albums}
    {wrapped_time}
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
    parser = argparse.ArgumentParser("main.py")
    args = __get_args(parser)
    if args["mode"] == "pull":
        main_pull(args["testing"])
    elif args["mode"] == "kafka":
        main_kafka()
    else:
        parser.print_help()
        raise ValueError("Invalid arguments")

import os
import logging
import requests
from typing import Dict, Iterator, Tuple, Any


class ApiHandler:
    def __init__(self, testing: bool = False) -> None:
        self.session = requests.session()
        self.token = self.__get_token(testing)
        self.headers = self.__make_headers()
        self.base_url = "https://api.spotify.com/v1/"

    def __get_token(self, testing: bool) -> str:
        if testing:
            return self.__get_testing_token()
        else:
            return self.__get_token_from_request()

    def __get_testing_token(self) -> str:
        try:
            logging.info('USING "API_TESTING_TOKEN"')
            return os.environ["API_TESTING_TOKEN"]
        except KeyError:
            logging.warning('MISSING "API_TESTING_TOKEN" ENV VAR')
            return self.__get_token_from_request()

    def __get_token_from_request(self) -> str:
        url = f"https://accounts.spotify.com/api/token"
        payload = self.__make_token_payload()
        response = self.session.post(url, data=payload)
        logging.debug(f"TOKEN RESPONSE CODE: {response.status_code}")
        return response.json()["access_token"]

    def __make_token_payload(self) -> Dict[str, str]:
        return {
            "grant_type": "client_credentials",
            "client_id": os.environ["API_CLIENT_ID"],
            "client_secret": os.environ["API_CLIENT_SECRET"],
        }

    def __make_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def __get_endpoint_results(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, headers=self.headers)
        return response.json()

    def __parse_offset_and_limit(self, url: str) -> Tuple[int, ...]:
        if url is None:
            return (0, 0)
        else:
            parsed = url.split("&")[-2:]
            map_parsed = map(lambda x: int(x.split("=")[-1]), parsed)
            return tuple(map_parsed)

    def get_new_releases(
        self, country: str = "US", limit: int = 20, offset: int = 0
    ) -> Iterator[Dict[str, Any]]:
        url = (
            f"{self.base_url}"
            f"browse/new-releases?country={country}&offset={offset}&limit={limit}"
        )
        logging.info("PULLING NEW RELEASES...")
        while url is not None:
            logging.debug(f"NEW RELEASES URL: {url}")
            logging.info(f"\t{offset} - {offset + limit}")
            result = self.__get_endpoint_results(url)
            url = result["albums"]["next"]
            offset, limit = self.__parse_offset_and_limit(url)
            yield result["albums"]["items"]

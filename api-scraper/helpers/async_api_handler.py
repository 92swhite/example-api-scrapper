import os
import logging
import asyncio
import aiohttp
from aiohttp import ClientSession
from typing import Dict, Iterator, Tuple, Any


class ApiHandler:
    def __init__(self, testing: bool = False) -> None:
        pass

    async def async_init(self, testing: bool = False) -> None:
        self.token = await self.__get_token(testing)
        self.headers = self.__make_headers()
        self.base_url = "https://api.spotify.com/v1/"

    async def __get_token(self, testing: bool) -> str:
        if testing:
            token = await self.__get_testing_token()
        else:
            token = await self.__get_token_from_request()
        return token

    async def __get_testing_token(self) -> str:
        try:
            logging.info('USING "API_TESTING_TOKEN"')
            return os.environ["API_TESTING_TOKEN"]
        except KeyError:
            logging.warning('MISSING "API_TESTING_TOKEN" ENV VAR')
            token = await self.__get_token_from_request()
            return token

    async def __make_request(
        self, url: str, headers: Dict[str, str] = {}, payload: Dict[str, str] = {}
    ) -> Dict[str, Any]:
        async with ClientSession() as session:
            response = await session.post(url, data=payload, headers=headers)
        response.raise_for_status()
        response_json = await response.json()
        return response_json

    async def __get_token_from_request(self) -> str:
        url = f"https://accounts.spotify.com/api/token"
        payload = self.__make_token_payload()
        response_json = await self.__make_request(url, payload=payload)
        return response_json["access_token"]

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

    async def __get_endpoint_results(self, url: str) -> Dict[str, Any]:
        response_json = await self.__make_request(url, headers=self.headers)
        return response_json

    def __parse_offset_and_limit(self, url: str) -> Tuple[int, ...]:
        if url is None:
            return (0, 0)
        else:
            parsed = url.split("&")[-2:]
            map_parsed = map(lambda x: int(x.split("=")[-1]), parsed)
            return tuple(map_parsed)

    async def get_new_releases(
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
            result = await self.__get_endpoint_results(url)
            url = result["albums"]["next"]
            offset, limit = self.__parse_offset_and_limit(url)
            yield result["albums"]["items"]

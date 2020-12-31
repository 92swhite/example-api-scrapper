import os
import logging
import requests


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
            logging.error('MISSING "API_TESTING_TOKEN" ENV VAR')
            return self.__get_token_from_request()

    def __get_token_from_request(self) -> str:
        url = f"https://accounts.spotify.com/api/token"
        payload = self.__make_token_payload()
        response = self.session.post(url, data=payload)
        logging.debug(f"TOKEN RESPONSE CODE: {response.status_code}")
        return response.json()["access_token"]

    def __make_token_payload(self) -> dict:
        return {
            "grant_type": "client_credentials",
            "client_id": os.environ["API_CLIENT_ID"],
            "client_secret": os.environ["API_CLIENT_SECRET"],
        }

    def __make_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def __get_endpoint_results(self, endpoint: str) -> dict:
        response = self.session.get(self.base_url + endpoint, headers=self.headers)
        return response.json()

    def get_new_releases(
        self, country: str = "US", limit: int = 20, offset: int = 0
    ) -> list:
        endpoint = (
            f"browse/new-releases?country={country}&offset={offset}&limit={limit}"
        )
        logging.debug(f"NEW RELEASES ENDPOINT: {endpoint}")
        logging.info(f"PULLING NEW RELEASES...\n\tOFFSET: {offset}\tLIMIT: {limit}")
        result = self.__get_endpoint_results(endpoint)
        return result["albums"]["items"]

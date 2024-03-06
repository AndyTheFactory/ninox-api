from json import JSONDecodeError
import requests
import logging
from typing import Optional


class NinoxApiError(Exception):
    pass


class NinoxApi:

    def __init__(
        self,
        api_key,
        base_url: str = "https://api.ninox.com",
        version: str = "v1",
        skip_ssl_validation: bool = False,
        logger: Optional[logging.Logger] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.version = version
        self.skip_ssl_validation = skip_ssl_validation
        self.logger = logger or logging.getLogger(__name__)
        self.url = f"{self.base_url}/{self.version}"

    def request(self, method, endpoint, data=None, params=None, files=None):
        url = f"{self.url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self.logger.debug(
            "Sending %s request to %s using data %s and params %s",
            method,
            url,
            data,
            params,
        )

        try:
            res = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                files=files,
                verify=not self.skip_ssl_validation,
            )
        except requests.exceptions.RequestException as e:
            self.logger.error("Request failed: %s", e)
            raise NinoxApiError(f"Request failed: {e}") from e

        if not (299 >= res.status_code >= 200):
            self.logger.error(
                "Request %s failed with status code %s and response: %s",
                url,
                res.status_code,
                res.text,
            )
            raise NinoxApiError(f"Request failed with status code {res.status_code}")

        try:
            result_data = res.json()
        except (ValueError, JSONDecodeError) as e:
            self.logger.error(
                "When requesting %s , Failed to decode response: %s", url, res.text
            )
            raise NinoxApiError(f"Failed to decode response: {res.text}") from e

        return result_data

    def get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, files=None):
        return self.request("POST", endpoint, data=data, files=None)

    def put(self, endpoint, data=None):
        return self.request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self.request("DELETE", endpoint)

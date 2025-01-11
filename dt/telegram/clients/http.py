import logging
import abc
import asyncio

import aiohttp
import httpx

from dt.config import BotConfig


class BaseApiClient(abc.ABC):
    def __init__(self, base_url: str, api_key: str, timeout: int):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    @abc.abstractmethod
    async def post(self, endpoint: str, payload: dict) -> dict:
        pass

    @abc.abstractmethod
    async def close(self):
        pass


class AioHttpApiClient(BaseApiClient):
    def __init__(self, base_url: str, api_key: str, timeout: int):
        super().__init__(base_url, api_key, timeout)
        self.session = aiohttp.ClientSession()

    async def post(self, endpoint: str, payload: dict) -> dict:
        """Make a POST request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        try:
            async with self.session.post(
                url, json=payload, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
            return {}

    async def close(self):
        """Close the AIOHTTP client."""
        await self.session.close()


class HttpxApiClient(BaseApiClient):
    def __init__(self, base_url: str, api_key: str, timeout: int = 10):
        super().__init__(base_url, api_key, timeout)

    async def post(self, endpoint: str, payload: dict) -> dict:
        """Make a POST request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, json=payload, headers=headers
                )
                response.raise_for_status()
                return response.json().get("response", [])
        except httpx.RequestError as e:
            logging.error(f"Request error while fetching vacancies: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP status error: {e}")
            raise
        except asyncio.TimeoutError:
            logging.error("Request timed out.")
            raise

    async def close(self):
        """Close the HTTPX client."""
        pass


class VacancyClient:
    def __init__(self, api_client: BaseApiClient):
        self.api_client = api_client

    async def fetch_vacancies(
        self, category_name: str, quantity_lines: int = 1
    ):
        """Fetch vacancies from the API."""
        payload = {
            "category": category_name,
            "quantity_lines": str(quantity_lines),
        }
        try:
            return await self.api_client.post(
                BotConfig.API_CLIENT_ENDPOINT, payload
            )
        except Exception as e:
            logging.error(f"Error fetching vacancies: {e}")
            return []

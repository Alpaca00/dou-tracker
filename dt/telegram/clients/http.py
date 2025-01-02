import os

import aiohttp
import logging

from dotenv import load_dotenv

load_dotenv()


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_key = os.environ.get("API_KEY")
        self.session = aiohttp.ClientSession()

    async def send_request(self, endpoint: str, payload: dict) -> dict:
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
                response_data = await response.json()
                return response_data
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
            return {}

    async def close(self):
        await self.session.close()

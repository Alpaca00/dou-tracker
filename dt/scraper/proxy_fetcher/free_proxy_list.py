import ast
import asyncio

import aiohttp
from aiohttp import ClientError, ClientTimeout
from bs4 import BeautifulSoup, Tag, NavigableString
from loguru import logger as l

from dt.extension import conf


class ProxyFetcherFreeProxyList:
    def __init__(
        self,
        proxy_origin_host: str = conf.SCRAPER.proxy_origin_host,
        proxy_fallback_host: str = conf.SCRAPER.proxy_fallback_host,
        proxy_verify_host: str = conf.SCRAPER.proxy_verify_host,
        debug: bool = bool(ast.literal_eval(conf.GLOBAL.logging)),
    ):
        self.proxy_origin_host = proxy_origin_host
        self.proxy_fallback_host = proxy_fallback_host
        self.proxy_verify_host = proxy_verify_host
        self.proxies = []
        self.debug = debug

    async def fetch_proxies(self):
        """Fetches a list of proxies from URL."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.proxy_origin_host
                ) as response:
                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    proxy_table = soup.find(
                        "table",
                        attrs={
                            "class": "table table-striped table-bordered"
                        },
                    )
                    self.proxies = await self._parse_proxies(proxy_table)

                    if self.proxies:
                        if self.debug:
                            l.debug("Proxies found:")
                            for proxy in self.proxies:
                                l.debug(proxy)
                    else:
                        if self.debug:
                            l.debug("Failed to find proxies.")
                        self.proxies = [self.proxy_fallback_host]

        except aiohttp.ClientError as e:
            l.debug(f"Error loading page: {e}")
            self.proxies = [self.proxy_fallback_host]

    @staticmethod
    async def _parse_proxies(proxy_table: Tag | NavigableString | None):
        """Parses the proxy table and returns a list of proxies."""
        proxies = []
        if proxy_table:
            rows = proxy_table.find_all("tr")
            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) > 1:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    https = cols[6].text.strip().lower() == "yes"
                    protocol = "https" if https else "http"
                    proxies.append(f"{protocol}://{ip}:{port}")
        return proxies

    async def check_proxy(self, proxy: str):
        """Checks if the proxy is working by sending a request to a URL."""
        try:
            timeout = ClientTimeout(total=5)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.proxy_verify_host, proxy=proxy, timeout=timeout
                ) as response:
                    if response.status == 200:
                        if self.debug:
                            l.debug(f"Proxy {proxy} is available.")
                        return proxy
                    else:
                        if self.debug:
                            l.debug(f"Proxy {proxy} is not available.")
                        return None
        except (ClientError, asyncio.TimeoutError) as e:
            if self.debug:
                l.debug(f"Error checking proxy {proxy}: {e}")
            return None

    async def check_all_proxies(self):
        """Checks all proxies for availability."""
        for proxy in self.proxies:
            valid_proxy = await self.check_proxy(proxy)
            if valid_proxy:
                return valid_proxy

        if self.debug:
            l.debug("No working proxies found, returning local address.")
        return self.proxy_fallback_host

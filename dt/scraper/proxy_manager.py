from typing import Optional
from dt.scraper.proxy_fetcher.proxy_manager import proxy_fetcher_


class ProxyManager:
    """Manage proxy fetching and usage."""

    def __init__(self, proxy_fetcher: proxy_fetcher_):
        self.proxy_fetcher = proxy_fetcher
        self.proxy: Optional[str] = None

    async def get_working_proxy(self) -> Optional[str]:
        """Get a working proxy by checking each proxy in the list."""
        await self.proxy_fetcher.fetch_proxies()
        for _ in range(len(self.proxy_fetcher.proxies)):
            proxy = self.proxy_fetcher.proxies.pop(0)
            if not proxy:
                self.proxy = None
            working_proxy = await self.proxy_fetcher.check_proxy(proxy)
            if working_proxy:
                self.proxy = working_proxy
                print(f"Using proxy: {self.proxy}")
                return self.proxy
        return None

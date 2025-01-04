from dt.config import ScrapperConfig


def proxy_fetcher_():
    """Returns a proxy fetcher based on the URL."""
    match ScrapperConfig.PROXY_ORIGIN_HOST:
        case "https://free-proxy-list.net/":
            from dt.scraper.proxy_fetcher.free_proxy_list import (
                ProxyFetcherFreeProxyList,
            )

            return ProxyFetcherFreeProxyList()
        case _:
            raise ValueError("Unknown proxy URL")

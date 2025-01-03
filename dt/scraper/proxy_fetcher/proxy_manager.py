from dt.extension import conf


def proxy_fetcher_():
    """Returns a proxy fetcher based on the URL."""
    match conf.URI.proxy_origin_host:
        case "https://free-proxy-list.net/":
            from dt.scraper.proxy_fetcher.free_proxy_list import (
                ProxyFetcherFreeProxyList,
            )

            return ProxyFetcherFreeProxyList()
        case _:
            raise ValueError("Unknown proxy URL")

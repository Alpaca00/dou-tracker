import asyncio
import sys

from loguru import logger

from dt.scraper.models import JobCategories
from dt.scraper.proxy_fetcher.free_proxy_list import (
    ProxyFetcherFreeProxyList,
)
from dt.scraper.proxy_manager import ProxyManager
from dt.scraper.vacancy_scraper import VacancyScraper

logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    format="{time:DD:MM:YYYY HH:mm:ss} | {level} | {message}",
)
logger.add(
    "app.log",
    rotation="1 day",
    retention="2 days",
    level="DEBUG",
    format="{time:DD:MM:YYYY HH:mm:ss} | {level} | {message}",
)


async def main() -> None:
    """The main function to run the vacancy scraper."""
    from dt.scraper.proxy_fetcher.proxy_manager import proxy_fetcher_

    proxy_fetcher = proxy_fetcher_()
    proxy_manager = ProxyManager(proxy_fetcher)

    scraper = VacancyScraper(
        url="https://jobs.dou.ua/vacancies/?category=" + JobCategories.QA.value,
        # proxy_manager=proxy_manager,
    )

    await scraper.fetch_page()
    vacancies = scraper.parse_vacancies()
    scraper.print_vacancies(vacancies)

if __name__ == "__main__":
    asyncio.run(main())

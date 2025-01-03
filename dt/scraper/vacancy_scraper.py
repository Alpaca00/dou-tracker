from datetime import datetime
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from dt.scraper.models import MONTHS_MAPPING
from dt.scraper.vacancy import IVacancy
from dt.scraper.proxy_manager import ProxyManager


class VacancyScraper:
    """A scraper for extracting job vacancies from a web page."""

    def __init__(
        self,
        url: str,
        proxy_manager: Optional[ProxyManager] = None,
        headers: Optional[dict] = None,
    ):
        self.url = url
        self.proxy_manager = proxy_manager
        self.headers = headers or {
            "User-Agent": generate_user_agent(device_type="desktop")
        }
        self.soup: Optional[BeautifulSoup] = None
        self.proxy = None

    async def fetch_page(self) -> None:
        """Fetches the HTML content of the job listings."""
        if self.proxy_manager:
            if not self.proxy:
                self.proxy = await self.proxy_manager.get_working_proxy()

        async with aiohttp.ClientSession() as session:
            try:
                if self.proxy:
                    async with session.get(
                        self.url, headers=self.headers, proxy=self.proxy
                    ) as response:
                        response.raise_for_status()
                        content = await response.text()
                        self.soup = BeautifulSoup(content, "html.parser")
                else:
                    async with session.get(
                        self.url, headers=self.headers
                    ) as response:
                        response.raise_for_status()
                        content = await response.text()
                        self.soup = BeautifulSoup(content, "html.parser")
            except aiohttp.ClientError as e:
                print(
                    f"Failed to load the page with proxy {self.proxy}: {e}"
                )
                if self.proxy:
                    self.proxy = None
                    await self.fetch_page()
            except Exception as e:
                print(f"Unexpected error occurred: {e}")

    def parse_vacancies(self, quantity_lines: int = 1) -> list[IVacancy]:
        """Parses the job vacancies listed on the lines."""
        if not self.soup:
            raise Exception(
                "Page content not loaded. Please call fetch_page() first."
            )

        date = datetime.now() if quantity_lines == 1 else None
        vacancies_list = self.soup.find("ul", class_="lt")
        date_vacancies: list[IVacancy] = []

        # not implemented, just for testing purposes
        if 1 < quantity_lines < 7:
            return date_vacancies

        if vacancies_list:
            vacancies = vacancies_list.find_all("li", class_="l-vacancy")
            for vacancy in vacancies:
                date_text = (
                    vacancy.find("div", class_="date").text.strip()
                    if vacancy.find("div", class_="date")
                    else None
                )
                if date_text and self._is_contains_date(date_text, date):
                    date_vacancies.append(
                        self._extract_vacancy_info(vacancy)
                    )

        return date_vacancies

    @staticmethod
    def _is_contains_date(date_text: str, date: datetime) -> bool:
        """Determines if the date text contains date."""
        date_parts = date_text.split()
        if len(date_parts) == 2:
            day, month_name = date_parts
            day = int(day)
            month = MONTHS_MAPPING.get(month_name.lower())
            return month and month.value == date.month and day == date.day
        return False

    @staticmethod
    def _extract_vacancy_info(vacancy) -> IVacancy:
        """Extracts detailed information about a single vacancy."""
        title_tag = vacancy.find("a", class_="vt")
        title = (
            title_tag.text.strip() if title_tag else "No title available"
        )
        link = title_tag["href"] if title_tag else "No link available"
        company_tag = vacancy.find("a", class_="company")
        company = (
            company_tag.text.strip()
            if company_tag
            else "No company available"
        )
        location = (
            vacancy.find("span", class_="cities").text.strip()
            if vacancy.find("span", class_="cities")
            else "No location available"
        )
        description = (
            vacancy.find("div", class_="sh-info").text.strip()
            if vacancy.find("div", class_="sh-info")
            else "No description available"
        )

        return IVacancy(title, link, company, location, description)

    @staticmethod
    def print_vacancies(vacancies: list[IVacancy]) -> None:
        """Prints the list of job vacancies."""
        if not vacancies:
            print("No job vacancies found for today.")
        else:
            print(
                f"Found {len(vacancies)} job vacancies posted today:\n"
                + "*" * 40
            )
            for vacancy in vacancies:
                print(f"Title: {vacancy.title}")
                print(f"Link: {vacancy.link}")
                print(f"Company: {vacancy.company}")
                print(f"Location: {vacancy.location}")
                print(f"Description: {vacancy.description}")
                print("-" * 40)

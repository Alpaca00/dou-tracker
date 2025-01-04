import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from dt.config import ServerConfig, ScrapperConfig
from dt.scraper.models import JobCategories, QuantityLines
from dt.scraper.vacancy_scraper import VacancyScraper


class VacancyRequest(BaseModel):
    category: JobCategories
    quantity_lines: QuantityLines


app = FastAPI(
    title=ServerConfig.TITLE,
    description=ServerConfig.DESCRIPTION,
    version=ServerConfig.SERVER_VERSION,
)


@app.get(f"/api/{ServerConfig.API_VERSION}/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "up"}


@app.post(f"/api/{ServerConfig.API_VERSION}/dou/vacancies")
async def dou_vacancies(
    data: VacancyRequest,
    api_key: str = Header(..., description="API key for authentication"),
):
    """
    Fetches job vacancies from the DOU website.

    - **category**: The category of the job vacancy. Available categories:
        - .NET
        - Account Manager
        - AI/ML
        - Analyst
        - Android
        - Animator
        - Architect
        - Artist
        - Assistant
        - Big Data
        - Blockchain
        - C++
        - C-level
        - Copywriter
        - Data Engineer
        - Data Science
        - DBA
        - Design
        - DevOps
        - Embedded
        - Engineering Manager
        - Erlang
        - ERP/CRM
        - Finance
        - Flutter
        - Front End
        - Golang
        - Hardware
        - HR
        - iOS/macOS
        - Java
        - Legal
        - Marketing
        - Node.js
        - Office Manager
        - Other
        - PHP
        - Product Manager
        - Project Manager
        - Python
        - QA
        - React Native
        - Ruby
        - Rust
        - Sales
        - Salesforce
        - SAP
        - Scala
        - Scrum Master
        - Security
        - SEO
        - Support
        - SysAdmin
        - Technical Writer
        - Unity
        - Unreal Engine
        - Військова справа

    - **quantity_lines**: The number of pages to fetch vacancies from. The maximum value is 1 right now.
        - 1

    - **api_key**: The API key for the request (passed via header).

    **Responses:**
    - 200: Successful retrieval of vacancies.
    - 400: Missing category or day in the request.
    - 403: Invalid API key provided.
    """
    if api_key != ServerConfig.API_KEY:
        raise HTTPException(
            status_code=403, detail="(error) invalid API key"
        )
    category = data.category.value
    lines = data.quantity_lines
    if category is None or lines is None:
        raise HTTPException(
            status_code=400,
            detail="(error) missing category or quantity_lines",
        )

    scraper = VacancyScraper(
        url=f"{ScrapperConfig.MAIN_HOST}/vacancies/?category={category}",
    )

    await scraper.fetch_page()
    vacancies = scraper.parse_vacancies(quantity_lines=int(lines))
    return {"response": vacancies}

import sys
import os
from datetime import timedelta
import logging

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

import asyncio
import httpx
from dotenv import load_dotenv

from dt.telegram.db.session import initialize_database
from dt.telegram.helpers.formatter import format_html_job_listing
from dt.scraper.models import JobCategories


load_dotenv()
API_KEY = os.environ.get("API_KEY")


def setup_categories(categories: dict):
    """Setup categories in PostgreSQL."""
    db = initialize_database()
    for name, description in categories.items():
        db.add_category(name, description)


async def save_to_postgres(category_name, new_data):
    """Save data to PostgreSQL."""
    db = initialize_database()
    db.add_category(category_name)
    for job in new_data:
        db.add_job(
            title=job["title"],
            company=job["company"],
            location=job["location"],
            description=job["description"],
            link=job["link"],
            formatted="<code>-------------------------</code>",
            category_name=category_name,
        )


async def compare_postgres_documents(category_name, new_data):
    """Compare new job data with existing records in PostgreSQL."""
    db = initialize_database()
    existing_category = db.get_category_by_name(category_name)
    if not existing_category:
        return []
    jobs_by_category = db.get_jobs_by_category(category_name)

    new_jobs = [
        job for job in new_data if job["link"] not in jobs_by_category
    ]
    return new_jobs


async def check_vacancies(bot_handler, category_name):
    """Check vacancies from the DOU website and notify about changes."""
    payload = {"category": category_name, "quantity_lines": "1"}
    url = "http://app:5000/api/v1/dou/vacancies"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                url, json=payload, headers=headers
            )
            response.raise_for_status()

            new_data = response.json().get("response", [])
            new_jobs = await compare_postgres_documents(
                category_name, new_data
            )

            if new_jobs:
                await save_to_postgres(category_name, new_data)

                job_listings = "\n".join(
                    [
                        format_html_job_listing(
                            job=job, category=category_name
                        )
                        for job in new_jobs
                    ]
                )

                await bot_handler.bot.send_message(
                    chat_id=1319159640,
                    text=job_listings,
                    parse_mode="HTML",
                )
            else:
                logging.info("No new or changed job listings.")
    except httpx.RequestError as e:
        logging.error(f"An error occurred while requesting data: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
    except asyncio.TimeoutError:
        logging.error("Request timed out.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


async def job_function(bot_handler, category_name):
    """Job function to check vacancies."""
    await check_vacancies(bot_handler, category_name)


def schedule_categories_jobs(scheduler, bot_handler, start_time):
    """Schedules jobs for all categories with intervals and descriptions."""
    all_categories = JobCategories.get_all_categories()
    categories = {}

    for item, category in enumerate(all_categories, start=1):
        category_name = category.value
        interval_seconds = 30
        start_date = start_time + timedelta(
            seconds=(item - 1) * interval_seconds
        )

        categories[category_name] = (
            f"Category: {category_name} | "
            f"Job Index: {item} | "
            f"Start Time: {start_date.strftime('%d-%m-%Y %H:%M:%S')} | "
            f"Interval: {interval_seconds} seconds"
        )

        scheduler.add_job(
            job_function,
            "interval",
            seconds=interval_seconds,
            start_date=start_date,
            args=[bot_handler, category_name],
        )

    return categories

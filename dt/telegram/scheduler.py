import sys
import os
from datetime import timedelta
import logging

from apscheduler.triggers.cron import CronTrigger

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from dt.telegram.clients.http import VacancyClient, HttpxApiClient
from dt.config import ServerConfig, BotConfig
from dt.telegram.db.session import initialize_database
from dt.telegram.helpers.formatter import format_html_job_listing
from dt.scraper.models import JobCategories


def setup_categories(categories: dict):
    """Setup categories in PostgreSQL."""
    db = initialize_database()
    db.delete_categories()
    for name, description in categories.items():
        db.add_category(name, description)


def clear_jobs():
    """Clear all jobs in PostgreSQL."""
    db = initialize_database()
    db.delete_all_jobs()


def get_all_chat_ids_by_subscription(category_name):
    """Get all chat IDs by subscription."""
    db = initialize_database()
    return db.get_chat_ids_by_subscription(category_name)


def save_to_postgres(category_name, new_data):
    """Save data to PostgreSQL."""
    db = initialize_database()
    for job in new_data:
        db.add_job(
            title=job["title"],
            company=job["company"],
            location=job["location"],
            description=job["description"],
            link=job["link"],
            formatted="\n",
            category_name=category_name,
        )


def compare_postgres_documents(category_name, new_data):
    """Compare new job data with existing records in PostgreSQL."""
    db = initialize_database()
    jobs_by_category = db.get_jobs_by_category(category_name)
    links = [job.link for job in jobs_by_category]
    new_jobs = [job for job in new_data if job["link"] not in links]
    return new_jobs


async def check_vacancies(bot_handler, category_name):
    """Check vacancies from the DOU website and notify about changes."""
    api_client = HttpxApiClient(
        base_url=BotConfig.API_CLIENT_BASE_URL,
        api_key=ServerConfig.API_KEY,
        timeout=BotConfig.API_CLIENT_TIMEOUT,
    )
    vacancy_client = VacancyClient(api_client=api_client)
    try:
        new_data = await vacancy_client.fetch_vacancies(category_name)

        new_jobs = compare_postgres_documents(category_name, new_data)

        if new_jobs:
            save_to_postgres(category_name, new_data)
            chat_ids = get_all_chat_ids_by_subscription(category_name)
            for chat_id in chat_ids:
                for job in new_jobs:
                    job_listing = format_html_job_listing(
                        job=job, category=category_name
                    )
                    await bot_handler.bot.send_message(
                        chat_id=chat_id,
                        text=job_listing,
                        parse_mode="HTML",
                    )
        else:
            logging.info("No new or changed job listings.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


async def job_function(bot_handler, category_name):
    """Job function to check vacancies."""
    await check_vacancies(bot_handler, category_name)


def schedule_categories_jobs(scheduler, bot_handler, start_time):
    """Schedules jobs for all categories with intervals and descriptions."""
    all_categories = JobCategories.get_all_categories()
    categories = {}

    scheduler.add_job(
        clear_jobs,
        trigger=CronTrigger(hour=0, minute=0, second=0),
        id="clear_jobs_task",
        replace_existing=True,
    )
    for item, category in enumerate(all_categories, start=1):
        category_name = category.value
        interval_seconds = BotConfig.SCHEDULER_INTERVAL
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

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import json
import logging
import os
import sys
import asyncio

import aiofiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
from deepdiff import DeepDiff
from dotenv import load_dotenv

from dt.telegram.bot import BotHandler
from dt.telegram.config.bot_config import TOKEN
from dt.telegram.helpers.formatter import format_html_job_listing


load_dotenv()
API_KEY = os.environ.get("API_KEY")


async def save_to_file_async(data, filename):
    """Save data to a file asynchronously."""
    async with aiofiles.open(filename, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))


def compare_json_objects(file1: str, file2: str) -> dict:
    """Compare two JSON files and return differences."""
    if not os.path.exists(file1) or not os.path.exists(file2):
        return {}

    with open(file1, "r", encoding="utf-8") as f1, open(
        file2, "r", encoding="utf-8"
    ) as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)

    diff = DeepDiff(json1, json2, ignore_order=True)
    return diff


async def check_vacancies(bot_handler):
    """Check vacancies from the DOU website and notify about changes."""
    payload = {"category": "QA", "quantity_lines": "1"}
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

            data = response.json()

            if os.path.exists("QA-last.json"):
                os.rename("QA-last.json", "QA-first.json")

            await save_to_file_async(data, "QA-last.json")

            diff = compare_json_objects("QA-first.json", "QA-last.json")
            if diff.get("values_changed") or diff.get(
                "dictionary_item_added"
            ):
                new_jobs = [
                    job
                    for job in data.get("response", [])
                    if f"root['response'][{data['response'].index(job)}]"
                    in diff.get("dictionary_item_added", {})
                ]

                job_listings = "\n".join(
                    [format_html_job_listing(job) for job in new_jobs]
                )

                if new_jobs:
                    await bot_handler.bot.send_message(
                        chat_id=1319159640,
                        text=job_listings,
                        parse_mode="HTML",
                    )
                else:
                    logging.info("No new or changed job listings.")
            else:
                logging.info("No differences found in job listings.")
    except httpx.RequestError as e:
        logging.error(f"An error occurred while requesting data: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
    except asyncio.TimeoutError:
        logging.error("Request timed out.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


async def job_function(bot_handler):
    """Job function to check vacancies."""
    await check_vacancies(bot_handler)


async def main():
    """Main entry point of the script."""
    bot_handler = BotHandler(bot_token=TOKEN)
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        job_function, "cron", minute="*/1", args=[bot_handler]
    )
    scheduler.start()

    await bot_handler.start_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

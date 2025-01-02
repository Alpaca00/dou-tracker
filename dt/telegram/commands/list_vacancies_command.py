import logging

from aiogram.enums import ParseMode
from aiogram import html
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from dt.scraper.models import JobCategories
from dt.telegram.clients.http import ApiClient
from dt.telegram.commands import Command
from dt.telegram.helpers.formatter import format_html_job_listing


class ListVacanciesCommand(Command):
    """Command to list job vacancies."""

    async def execute(self, callback_query):
        if callback_query.data == "list_vacancies":
            logging.info("User selected to list vacancies")

            category_buttons = [
                InlineKeyboardButton(
                    text=category.value,
                    callback_data=f"category_{category.value}",
                )
                for category in JobCategories.get_all_categories()
            ]

            category_buttons.append(
                InlineKeyboardButton(
                    text="❌ CLOSE", callback_data="close_categories"
                )
            )

            category_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[button] for button in category_buttons]
            )

            await callback_query.answer("Please select a job category:")
            await callback_query.message.answer(
                html.code("CHOOSE A CATEGORY"),
                reply_markup=category_keyboard,
                parse_mode=ParseMode.HTML,
            )

        elif callback_query.data.startswith("category_"):
            category = callback_query.data.split("_")[1]
            logging.info(f"User selected category: {callback_query.data}")
            await callback_query.answer(
                f"Searching for jobs in the '{category}' category..."
            )

            api_client = ApiClient(base_url="http://localhost:8000")

            payload = {"category": category, "quantity_lines": "1"}

            data = await api_client.send_request(
                "/api/v1/dou/vacancies", payload
            )
            if data:
                job_listings = "\n".join(
                    [
                        format_html_job_listing(job)
                        for job in data["response"]
                    ]
                )

                await callback_query.message.answer(
                    html.code(
                        f"Here are the latest job openings in {category} category"
                    ),
                    parse_mode=ParseMode.HTML,
                )
                await callback_query.message.answer(
                    job_listings, parse_mode=ParseMode.HTML
                )
            else:
                logging.warning("No data received or request failed.")

            await api_client.close()

        elif callback_query.data == "close_categories":
            logging.info("User closed the menu")
            await callback_query.answer("Menu closed.")
            await callback_query.message.answer(
                "You can use other commands or type your request."
            )

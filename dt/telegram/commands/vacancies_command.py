from aiogram.enums import ParseMode
from aiogram import html
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from dt.scraper.models import JobCategories
from dt.telegram.commands import Command


class VacanciesCommand(Command):
    """Command to list job vacancies."""

    async def execute(self, message):

        if message.text == f"{self.prefix}vacancies":

            category_buttons = [
                InlineKeyboardButton(
                    text=category.value,
                    callback_data=f"category_{category.value}",
                )
                for category in JobCategories.get_all_categories()
            ]

            category_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[button] for button in category_buttons]
            )

            await message.answer(
                html.quote("Оберіть категорію вакансій"),
                reply_markup=category_keyboard,
                parse_mode=ParseMode.HTML,
            )

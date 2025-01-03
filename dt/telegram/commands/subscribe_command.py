import json
from aiogram import html
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

from dt.scraper.models import JobCategories
from dt.telegram.commands import Command


SUBSCRIPTIONS_FILE = "subscriptions.json"


class SubscribeVacanciesCommand(Command):

    async def execute(self, message):
        if message.text == f"{self.prefix}subscribe":
            category_buttons = [
                InlineKeyboardButton(
                    text=category.value,
                    callback_data=f"subscribe_{category.value}",
                )
                for category in JobCategories.get_all_categories()
            ]

            category_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[button] for button in category_buttons]
            )

            await message.answer(
                html.code("Оберіть категорію вакансій"),
                reply_markup=category_keyboard,
                parse_mode=ParseMode.HTML,
            )

    async def handle_subscribe_selection(self, callback_query):
        category = callback_query.data.split("_")[1]

        user_id = callback_query.from_user.id
        self.save_subscription(user_id, category)

        await callback_query.message.answer(
            html.code(
                f"Ви підписались на отримання вакансій категорії {category}"
            ),
            parse_mode=ParseMode.HTML,
        )

    @staticmethod
    def save_subscription(user_id, category):
        try:
            with open(SUBSCRIPTIONS_FILE, "r") as file:
                subscriptions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            subscriptions = {}

        subscriptions[user_id] = category

        with open(SUBSCRIPTIONS_FILE, "w") as file:
            json.dump(subscriptions, file, indent=4)

    @staticmethod
    def list_subscriptions():
        try:
            with open(SUBSCRIPTIONS_FILE, "r") as file:
                subscriptions = json.load(file)
            return subscriptions
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

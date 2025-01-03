from aiogram import html
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

from dt.telegram.commands import Command
from dt.telegram.db.session import initialize_database


class UnsubscribeVacanciesCommand(Command):
    """Command to unsubscribe from job categories."""

    async def execute(self, message):
        if message.text == f"{self.prefix}unsubscribe":
            db = initialize_database()
            user_subscriptions = db.get_user_subscriptions(
                user_id=message.from_user.id
            )
            category_buttons = [
                InlineKeyboardButton(
                    text=category,
                    callback_data=f"unsubscribe_{category}",
                )
                for category in user_subscriptions
            ]

            category_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[button] for button in category_buttons]
            )

            await message.answer(
                html.quote("Оберіть категорію вакансій"),
                reply_markup=category_keyboard,
                parse_mode=ParseMode.HTML,
            )

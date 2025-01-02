from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram import html

from dt.telegram.commands import Command


class StartCommand(Command):
    """Command to handle /start command."""

    def __init__(self, inline_keyboard: InlineKeyboardMarkup):
        self.inline_keyboard = inline_keyboard

    async def execute(self, message: Message):
        await message.answer(
            text=html.code("WELCOME TO THE DOU SCRAPER BOT 🤖"),
            reply_markup=self.inline_keyboard,
            parse_mode=ParseMode.HTML,
        )

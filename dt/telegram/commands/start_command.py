from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram import html

from dt.telegram.commands import Command


class StartCommand(Command):
    """Command to handle /start command."""

    async def execute(self, message: Message):
        await message.answer(
            text=html.code(
                "Привіт! Я бот, який допоможе тобі cлідкувати за останніми вакансіями на сайті https://jobs.dou.ua/\nНаступним кроком буде вибір категорії вакансій, на які ти хочеш підписатись - обравши команду /subscribe\nТакож ти можеш переглянути останні вакансії за допомогою команди /vacancies"
            ),
            parse_mode=ParseMode.HTML,
        )

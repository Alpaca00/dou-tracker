from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram import html

from dt.telegram.commands import Command
from dt.telegram.db.session import initialize_database


class StartCommand(Command):
    """Command to handle /start command."""

    async def execute(self, message: Message):
        """Execute /start command."""
        db = initialize_database()
        current_user = db.get_user(user_id=str(message.from_user.id))
        if not current_user:
            db.add_user(
                user_id=str(message.from_user.id),
                chat_id=str(message.chat.id),
            )
        await message.answer(
            text=html.quote(
                "Привіт! Я бот, який допоможе тобі cлідкувати за останніми вакансіями на сайті https://jobs.dou.ua/"
                "\nНаступним кроком буде вибір категорії вакансій, на які хочеш підписатись - обравши команду /subscribe"
                "\nТакож можеш переглянути останні вакансії за допомогою команди /vacancies"
            ),
            parse_mode=ParseMode.HTML,
        )

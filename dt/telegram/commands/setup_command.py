from dataclasses import dataclass
from aiogram.types import BotCommand


@dataclass
class SetupCommandDescription:
    START: str = "розпочати роботу з ботом"
    VACANCIES: str = "отримати список сьогочнішніх вакансій"
    SUBSCRIBE: str = "підписатися на оновлення вакансій"
    UNSUBSCRIBE: str = "відписатися від оновлень вакансій"
    SUBSCRIPTIONS: str = "отримати список підписок"


async def setup_commands(bot_handler):
    descriptions = SetupCommandDescription()
    commands = [
        BotCommand(command=cmd.lower(), description=desc)
        for cmd, desc in descriptions.__dict__.items()
        if not cmd.startswith("__")
    ]
    await bot_handler.bot.delete_my_commands()
    await bot_handler.bot.set_my_commands(commands)

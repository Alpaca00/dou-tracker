from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command

from dt.telegram.commands import (
    CommandInvoker,
    StartCommand,
    VacanciesCommand,
    SubscribeVacanciesCommand,
    UnsubscribeVacanciesCommand,
    SubscriptionsCommand,
)


class BotHandler:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.dp = Dispatcher()
        self.bot = Bot(token=self.bot_token)
        self.invoker = CommandInvoker()

        self.invoker.register_command("start", StartCommand())
        self.invoker.register_command("vacancies", VacanciesCommand())
        self.invoker.register_command(
            "subscribe", SubscribeVacanciesCommand()
        )
        self.invoker.register_command(
            "unsubscribe", UnsubscribeVacanciesCommand()
        )
        self.invoker.register_command(
            "subscriptions", SubscriptionsCommand()
        )

    def register_handlers(self):
        """Register all handlers for the bot."""
        self.dp.message.register(
            self.command_start_handler, CommandStart()
        )
        self.dp.message.register(
            self.command_latest_vacancies_handler,
            Command(commands=["vacancies"]),
        )
        self.dp.message.register(
            self.command_subscribe_vacancies_handler,
            Command(commands=["subscribe"]),
        )
        self.dp.message.register(
            self.command_unsubscribe_vacancies_handler,
            Command(commands=["unsubscribe"]),
        )
        self.dp.message.register(
            self.command_subscriptions_handler,
            Command(commands=["subscriptions"]),
        )
        self.dp.callback_query.register(self.callback_query_handler)

    async def command_start_handler(self, message: Message):
        """Command handler for /start command."""
        await self.invoker.execute_command("start", message)

    async def command_latest_vacancies_handler(self, message: Message):
        """Command handler for /vacancies command."""
        await self.invoker.execute_command("vacancies", message)

    async def command_subscribe_vacancies_handler(self, message: Message):
        """Command handler for /subscribe command."""
        await self.invoker.execute_command("subscribe", message)

    async def command_unsubscribe_vacancies_handler(
        self, message: Message
    ):
        """Command handler for /unsubscribe command."""
        await self.invoker.execute_command("unsubscribe", message)

    async def command_subscriptions_handler(self, message: Message):
        """Command handler for /subscriptions command."""
        await self.invoker.execute_command("subscriptions", message)

    async def callback_query_handler(self, callback_query):
        """Handle callback queries."""
        if callback_query.data.startswith("category_"):
            await self.invoker.execute_category_command(callback_query)
        if callback_query.data.startswith("subscribe_"):
            await self.invoker.execute_subscribe_command(callback_query)
        elif callback_query.data.startswith("unsubscribe_"):
            await self.invoker.execute_unsubscribe_command(callback_query)
        else:
            await self.invoker.execute_command(
                callback_query.data, callback_query
            )

    async def start_polling(self):
        """Start the bot polling."""
        self.register_handlers()
        await self.dp.start_polling(self.bot)

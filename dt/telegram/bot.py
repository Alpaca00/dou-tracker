from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.filters import CommandStart

from dt.telegram.commands import (
    CommandInvoker,
    StartCommand,
    ListVacanciesCommand,
)


class BotHandler:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.dp = Dispatcher()
        self.bot = Bot(token=self.bot_token)
        self.invoker = CommandInvoker()

        self.add_subscription_button = InlineKeyboardButton(
            text="➕ Add subscription", callback_data="add_subscription"
        )
        self.remove_subscription = InlineKeyboardButton(
            text="❌ Remove subscription",
            callback_data="remove_subscription",
        )
        self.list_subscriptions = InlineKeyboardButton(
            text="📜 List subscriptions",
            callback_data="list_subscriptions",
        )
        self.list_vacancies = InlineKeyboardButton(
            text="📋 List vacancies", callback_data="list_vacancies"
        )
        self.inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [self.add_subscription_button, self.remove_subscription],
                [self.list_subscriptions, self.list_vacancies],
            ]
        )

        self.invoker.register_command(
            "start", StartCommand(self.inline_keyboard)
        )
        self.invoker.register_command(
            "list_vacancies", ListVacanciesCommand()
        )

    def register_handlers(self):
        """Register all handlers for the bot."""
        self.dp.message.register(
            self.command_start_handler, CommandStart()
        )
        self.dp.callback_query.register(self.callback_query_handler)

    async def command_start_handler(self, message: Message) -> None:
        """Command handler for /start command."""
        await self.invoker.execute_command("start", message)

    async def callback_query_handler(self, callback_query):
        """Handle callback queries."""
        if callback_query.data.startswith("category_"):
            category_name = callback_query.data.split("_")[1]
            await self.invoker.execute_category_command(
                category_name, callback_query
            )
        else:
            await self.invoker.execute_command(
                callback_query.data, callback_query
            )

    async def start_polling(self):
        """Start the bot polling."""
        self.register_handlers()
        await self.dp.start_polling(self.bot)

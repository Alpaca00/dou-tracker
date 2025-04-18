import logging

from aiogram.enums import ParseMode
from aiogram import html

from dt.config import BotConfig, ServerConfig
from dt.telegram.clients.http import AioHttpApiClient, VacancyClient
from dt.telegram.commands import Command
from dt.telegram.db.session import initialize_database
from dt.telegram.helpers.formatter import format_html_job_listing


class CommandInvoker:
    """Invoker class to handle command execution."""

    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, command: Command):
        self.commands[command_name] = command

    async def execute_command(self, command_name, *args):
        command = self.commands.get(command_name)
        if command:
            await command.execute(*args)
        else:
            logging.warning(f"Command '{command_name}' not found.")

    @staticmethod
    async def execute_category_command(callback_query):
        """Execute command dynamically for job category."""

        category = callback_query.data.split("_")[1]

        api_client = AioHttpApiClient(
            base_url=BotConfig.API_CLIENT_BASE_URL,
            api_key=ServerConfig.API_KEY,
            timeout=BotConfig.API_CLIENT_TIMEOUT,
        )
        vacancy_client = VacancyClient(api_client=api_client)
        data = await vacancy_client.fetch_vacancies(
            category_name=category, quantity_lines=1
        )
        if data:
            job_listings = "\n".join(
                [
                    format_html_job_listing(job=job, category=category)
                    for job in data["response"]
                ]
            )

            if data["response"]:
                await callback_query.message.answer(
                    html.quote(
                        f"Ось останні вакансії в категорії {category}"
                    ),
                    parse_mode=ParseMode.HTML,
                )

                await callback_query.message.answer(
                    job_listings, parse_mode=ParseMode.HTML
                )
            else:
                await callback_query.message.answer(
                    html.quote(
                        f"Сьогодні вакансій в категорії {category} ще не опубліковано, на превеликий жаль. Cпробуйте пізніше"
                    ),
                    parse_mode=ParseMode.HTML,
                )
        else:
            logging.warning("No data received or request failed.")

        await api_client.close()

    async def execute_subscribe_command(self, callback_query):
        """Execute command dynamically for job subscription."""
        command_name = callback_query.data.split("_")[0]
        subscription_name = callback_query.data.split("_")[1]
        command = self.commands.get(command_name)
        if command and command_name == "subscribe":
            db = initialize_database()
            user_subscriptions = db.get_user_subscriptions(
                user_id=callback_query.from_user.id
            )
            if (
                len(user_subscriptions)
                >= BotConfig.USER_SUBSCRIPTIONS_LIMIT
            ):
                await callback_query.message.answer(
                    html.quote(
                        "Ви не можете підписатись на більше 3 категорій вакансій"
                    ),
                    parse_mode=ParseMode.HTML,
                )
                return
            db.add_subscribe_vacancy(
                user_id=callback_query.from_user.id,
                subscription_name=subscription_name,
            )
            await callback_query.message.answer(
                f"Ви підписалися на вакансії категорії {subscription_name}"
            )
        else:
            logging.warning(f"Command '{command_name}' not found.")

    async def execute_unsubscribe_command(self, callback_query):
        """Execute command dynamically for job unsubscription."""
        command_name = callback_query.data.split("_")[0]
        subscription_name = callback_query.data.split("_")[1]
        command = self.commands.get(command_name)
        if command and command_name.startswith("unsubscribe"):
            db = initialize_database()
            db.delete_subscribe_vacancy(
                user_id=callback_query.from_user.id,
                subscription_name=subscription_name,
            )
            await callback_query.message.answer(
                html.quote(
                    f"Ви відписалися від вакансій категорії {subscription_name}"
                ),
                parse_mode=ParseMode.HTML,
            )
        else:
            logging.warning(f"Command '{command_name}' not found.")

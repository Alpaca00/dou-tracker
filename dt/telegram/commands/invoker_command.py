import logging

from aiogram.enums import ParseMode
from aiogram import html

from dt.telegram.clients.http import ApiClient
from dt.telegram.commands import Command
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

        api_client = ApiClient(base_url="http://app:5000")

        payload = {"category": category, "quantity_lines": "1"}

        data = await api_client.send_request(
            "/api/v1/dou/vacancies", payload
        )
        if data:
            job_listings = "\n".join(
                [format_html_job_listing(job) for job in data["response"]]
            )

            if data["response"]:
                await callback_query.message.answer(
                    html.code(
                        f"Ось останні вакансії в категорії {category}"
                    ),
                    parse_mode=ParseMode.HTML,
                )

                await callback_query.message.answer(
                    job_listings, parse_mode=ParseMode.HTML
                )
            else:
                await callback_query.message.answer(
                    html.code(
                        "Вакансій сьогодні немає, на превеликий жаль. Cпробуйте пізніше"
                    ),
                    parse_mode=ParseMode.HTML,
                )
        else:
            logging.warning("No data received or request failed.")

        await api_client.close()

    async def execute_subscribe_command(self, callback_query):
        """Execute command dynamically for job subscription."""
        command_name = callback_query.data.split("_")[0]
        command = self.commands.get(command_name)
        if command:
            await command.handle_subscribe_selection(callback_query)
        else:
            logging.warning(f"Command '{command_name}' not found.")

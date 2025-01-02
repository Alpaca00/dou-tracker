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
    async def execute_category_command(category_name, callback_query):
        """Execute command dynamically for job category."""
        logging.info(f"Executing command for category: {category_name}")

        api_client = ApiClient(base_url="http://localhost:8000")

        payload = {"category": category_name, "quantity_lines": "1"}

        data = await api_client.send_request(
            "/api/v1/dou/vacancies", payload
        )
        if data:
            job_listings = "\n".join(
                [format_html_job_listing(job) for job in data["response"]]
            )

            await callback_query.message.answer(
                html.code(
                    f"Here are the latest job openings in {category_name} category"
                ),
                parse_mode=ParseMode.HTML,
            )
            await callback_query.message.answer(
                job_listings, parse_mode=ParseMode.HTML
            )
        else:
            logging.warning("No data received or request failed.")

        await api_client.close()

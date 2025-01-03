from aiogram import html
from aiogram.enums import ParseMode

from dt.telegram.commands import Command
from dt.telegram.db.session import initialize_database


class SubscriptionsCommand(Command):
    """Command to show user subscriptions."""

    async def execute(self, message):
        if message.text == f"{self.prefix}subscriptions":
            db = initialize_database()
            user_subscriptions = db.get_user_subscriptions(
                user_id=message.from_user.id
            )
            await message.answer(
                html.quote(
                    f"Ваші підписки:\n{', '.join(user_subscriptions)}"
                ),
                parse_mode=ParseMode.HTML,
            )

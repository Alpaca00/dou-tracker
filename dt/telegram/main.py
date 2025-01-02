import logging
import sys
import asyncio

from dt.telegram.bot import BotHandler
from dt.telegram.config.bot_config import TOKEN


async def main():
    bot_handler = BotHandler(bot_token=TOKEN)
    await bot_handler.start_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

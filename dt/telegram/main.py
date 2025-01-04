import sys
import os
from datetime import datetime
import logging

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dt.telegram.bot import BotHandler
from dt.config import BotConfig
from dt.telegram.scheduler import (
    schedule_categories_jobs,
    setup_categories,
)


async def main():
    """Main entry point of the script."""
    bot_handler = BotHandler(bot_token=BotConfig.TELEGRAM_BOT_TOKEN)
    scheduler = AsyncIOScheduler()
    start_time = datetime.now()
    categories = schedule_categories_jobs(
        scheduler, bot_handler, start_time
    )
    setup_categories(categories)
    scheduler.start()
    await bot_handler.start_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

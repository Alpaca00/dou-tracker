#### Dou Tracker Bot

Helpful bot for tracking vacancies in the [Dou](https://jobs.dou.ua/) job board.

Telegram bot: [~~@DouTrackerBot~~](https://t.me/DouTrackerBot)  will be deleted soon and will no longer be supported.

#### Commands

- `/start` - start the bot.
- `/subscribe` - subscribe to the job board (limit 3).
- `/unsubscribe` - unsubscribe from the job board.
- `/vacancies` - show the latest vacancies.
- `/subscriptions` - show the list of subscriptions.

#### How to set up?

1. Create a new bot using [@BotFather](https://t.me/botfather) and get the token.
2. Create a new `.env` file to the root directory and added next variables
   ```env
    # Project settings
    API_KEY=<your dou api key>
    BOT_TELEGRAM_TOKEN=<your telegram bot token>
    # Database settings
    POSTGRES_USER=<your postgres user>
    POSTGRES_PASSWORD=<your postgres password>
    POSTGRES_DB=telegram_bot
    POSTGRES_HOST=postgres
   ```
3. Execute the following docker command to create the database and start the bot
   ```bash
   docker-compose up -d
   ```
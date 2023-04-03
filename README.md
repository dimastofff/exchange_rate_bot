# Exchange Rate Bot

This is a simple Telegram bot for fetching exchange rates built using the aiogram library. It includes basic command handling, callback query handling, and usage statistics tracking.

## Features

- Region and city selection through callback queries
- Getting actual exchange rates data from site https://myfin.by/
- Admin functionality
- Middleware for logging bot usage
- 5 minutes data caching in memory for avoiding duplicate requests during short time duration

## Configuration

Create a `.env` file in the project directory with the following contents:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ADMINS=comma_separated_admin_user_ids
```

Replace `your_telegram_bot_token_here` with the actual bot token provided by the BotFather on Telegram, and `comma_separated_admin_user_ids` with a comma-separated list of Telegram user IDs for the bot administrators.

## Running the Bot with Docker Compose

Make sure you have Docker and Docker Compose installed on your machine. If not, follow the installation instructions for [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

```bash
docker compose up --build --abort-on-container-exit
```

The bot will now be up and running, ready to receive messages and handle commands until you submit ```Ctrl + C```.

## License

[MIT](https://choosealicense.com/licenses/mit/)

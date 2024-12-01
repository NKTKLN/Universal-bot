# ♾️ Universal Bot

## 🗒 Description

This bot was created with the goal of simplifying the development and usage of Telegram bots. It allows you to easily add new features through plugins, integrating them into a single main bot. This eliminates the need to store and manage multiple bots with different functionalities in your Telegram account.

## 💾 Prerequisites

* [Python](https://www.python.org/)
* [Docker CE](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Bot Configuration

Before starting, make sure to edit the `.env` file with your own configuration.

Example:

```env
# Telegram Bot Settings
BOT_TOKEN="110201544:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
OWNER_ID=1234567890

# Database settings
DATABASE_URL="sqlite+aiosqlite:///db/database.db"
```

You can get your bot token by contacting [@BotFather](https://t.me/BotFather) on Telegram.

## 📝 Plugin Documentation

If you want to create your own plugins, you can find the documentation for writing plugins in the following file: [custom plugin documentation](https://github.com/NKTKLN/Universal-bot/blob/master/bot/custom_plugins/README.md).

## 🐳 Run in Docker

```bash
docker compose up --build -d
```

## 📝 ToDo

- [ ] Add the ability to store plugin data in the database
- [ ] Fix the need to reboot when loading a new version of the plugin
- [ ] Add the ability to update the bot in the settings

## 📃 License

All my apps are released under the MIT license, see [LICENSE.md](https://github.com/NKTKLN/Universal-bot/blob/master/LICENSE) for full text.

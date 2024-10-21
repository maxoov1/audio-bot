# Audio Telegram Bot

Bot

## Migrations

Use [`goose`](https://pressly.github.io/goose/) for database migrations
```sh
goose -dir ./migrations sqlite3 ./database.sqlite up
```

## Configuration

```sh
TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
TELEGRAM_BOT_USERNAME = "bot_username"
```

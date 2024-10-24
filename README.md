# Audio Telegram Bot

Bot

## Migrations

Use [`yoyo`](https://ollycope.com/software/yoyo/latest/) for database migrations
```sh
yoyo apply --database sqlite:///database.sqlite migrations/
```

## Configuration

```sh
TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
TELEGRAM_SUPER_ADMIN_USER_ID = "123456789"
```

## Run

### Docker
```sh
docker build -t audio-bot:latest .
docker run -e TELEGRAM_BOT_TOKEN="" -e TELEGRAM_SUPER_ADMIN_USER_ID="" audio-bot:latest
```

import asyncio
import logging
import os
import secrets
import sys

import aiogram

import database


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set")

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)
dispatcher = aiogram.Dispatcher()


def generate_unique_id(number_of_bytes: int = 8) -> str:
    return secrets.token_hex(number_of_bytes)


def get_command_arguments(text: str, start: int = 1) -> list[str]:
    return text.split()[start:]


def is_admin(user_id: int) -> bool:
    admins_user_ids = database.query_get_admins()
    return admins_user_ids and user_id in admins_user_ids


@dispatcher.message(aiogram.filters.Command("start", "get"))
async def start_command_handler(message: aiogram.types.Message) -> None:
    arguments = get_command_arguments(message.text)
    if len(arguments) < 1:
        return

    if audio_query_result := database.query_get_audio(arguments[0]):
        await message.reply_audio(audio_query_result["telegram_file_id"])


@dispatcher.message(aiogram.filters.Command("remove"))
async def remove_command_handler(message: aiogram.types.Message) -> None:
    if not is_admin(message.from_user.id):
        return

    arguments = get_command_arguments(message.text)
    if len(arguments) < 1:
        return

    generated_id = arguments[0]
    if database.query_remove_audio(generated_id):
        await message.reply(f"removed {generated_id}")


@dispatcher.message()
async def audio_message_handler(message: aiogram.types.Message) -> None:
    if not is_admin(message.from_user.id) or not message.audio:
        return

    generated_id = generate_unique_id()
    link = await aiogram.utils.deep_linking.create_start_link(message.bot, generated_id)
    if database.query_create_audio(generated_id, message.audio.file_id):
        await message.reply(link)


async def main() -> None:
    bot = aiogram.Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=aiogram.client.default.DefaultBotProperties(
            parse_mode=aiogram.enums.ParseMode.HTML
        ),
    )
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass

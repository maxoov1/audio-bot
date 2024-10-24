import asyncio
import secrets
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

import database


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    sys.exit("TELEGRAM_BOT_TOKEN is not set")

dispatcher = Dispatcher()


def generate_unique_id() -> str:
    return secrets.token_urlsafe(8)


def get_command_arguments(text: str) -> list[str]:
    return text.split()[1:]


def is_admin(user_id: int) -> bool:
    admins_user_ids = database.query_get_admins()
    return admins_user_ids and user_id in admins_user_ids


@dispatcher.message(Command("start", "get"))
async def start_command_handler(message: Message) -> None:
    arguments = get_command_arguments(message.text)
    if len(arguments) < 1:
        return

    audio_query_result = database.query_get_audio(arguments[0])
    if audio_query_result:
        await message.reply_audio(audio_query_result["telegram_file_id"])


@dispatcher.message(Command("remove"))
async def remove_command_handler(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    arguments = get_command_arguments(message.text)
    if len(arguments) < 1:
        return

    generated_id = arguments[0]

    if database.query_remove_audio(generated_id):
        await message.reply(f"removed {generated_id}")


@dispatcher.message()
async def audio_message_handler(message: Message) -> None:
    if not is_admin(message.from_user.id) or not message.audio:
        return

    generated_id = generate_unique_id()

    database.query_create_audio(generated_id, message.audio.file_id)
    await message.reply(
        await create_start_link(message.bot, generated_id),
    )


async def main() -> None:
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

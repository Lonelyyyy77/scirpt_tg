import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging

TOKEN = ""
router = Router()

logging.basicConfig(level=logging.INFO)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я твой бот и отвечаю только на команду /start.")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
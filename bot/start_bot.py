import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, DB_NAME

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            phone TEXT,
            code TEXT
        )
    ''')
    conn.commit()
    conn.close()



async def main():
    init_db()

    from handlers.user.share_num import router as user_share_router
    from handlers.admin.user_stat import router as admin_user_stat
    dp.include_router(user_share_router)
    dp.include_router(admin_user_stat)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
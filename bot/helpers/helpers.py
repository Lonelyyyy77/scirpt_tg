import sqlite3
from math import ceil

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.handlers.admin.user_stat import FILTER_STATE
from config import DB_NAME

PAGE_SIZE = 3



def create_user_data_file_admin_panel(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, phone, code FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if not user_data:
        return None

    name, username, phone, code = user_data
    username = f"@{username}" if username else "Не указан"

    file_path = f"user_{user_id}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"👤 Имя: {name}\n")
        file.write(f"🔗 Username: {username}\n")
        file.write(f"📱 Номер телефона: {phone}\n")
        file.write(f"🔢 Код подтверждения: {code if code else '—'}\n")

    return file_path


def get_navigation_kb(users, page, total_pages, admin_id):
    kb = InlineKeyboardBuilder()
    for user in users:
        user_id, name, username, phone, code = user
        username = f"@{username}" if username else "Не указан"
        kb.row(InlineKeyboardButton(text=f"📄 Скачать: {name}", callback_data=f"user_details:{user_id}"))
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_page:{page - 1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Вперёд", callback_data=f"next_page:{page + 1}"))
    if nav_buttons:
        kb.row(*nav_buttons)
    filter_status = "✅ Включен" if FILTER_STATE.get(admin_id, False) else "❌ Выключен"
    kb.row(InlineKeyboardButton(text=f"🔍 Показать только без кода ({filter_status})", callback_data="toggle_filter"))
    return kb.as_markup()


def format_users_page(page, only_without_code=False):
    users = get_users_admin_panel(only_without_code)
    if not users:
        return None, 1
    total_pages = ceil(len(users) / PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    users_on_page = users[start_index:end_index]
    return users_on_page, total_pages

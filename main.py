import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# =========================
# НАЛАШТУВАННЯ
# =========================

TOKEN = "8760064417:AAFj-QHNveWTjzGlVkVS0UCJzB17NLGMQpw"
ADMIN_ID = 1561352771
CHANNEL_USERNAME = "@UAhubPolska"

# =========================
# BOT
# =========================

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# =========================
# КНОПКИ
# =========================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔥 Робота"),
            KeyboardButton(text="🏠 Житло")
        ],
        [
            KeyboardButton(text="🛠 Послуги"),
            KeyboardButton(text="🚗 Перевезення")
        ],
        [
            KeyboardButton(text="📄 Документи"),
            KeyboardButton(text="📢 Реклама")
        ]
    ],
    resize_keyboard=True
)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    text = f"""
🇵🇱 <b>Вітаємо в UA HUB Polska!</b>

Тут українці в Польщі знаходять:

🔥 Роботу
🏠 Житло
🛠 Послуги
🚗 Перевезення
📄 Допомогу з документами

👇 Оберіть потрібний розділ нижче.
"""

    await message.answer(text, reply_markup=main_keyboard)

# =========================
# КАТЕГОРІЇ
# =========================

@dp.message(F.text == "🔥 Робота")
async def work(message: Message):
    await message.answer(
        "✍️ Надішліть вакансію одним повідомленням."
    )

@dp.message(F.text == "🏠 Житло")
async def home(message: Message):
    await message.answer(
        "🏠 Надішліть інформацію про житло."
    )

@dp.message(F.text == "🛠 Послуги")
async def services(message: Message):
    await message.answer(
        "🛠 Опишіть вашу послугу."
    )

@dp.message(F.text == "🚗 Перевезення")
async def transport(message: Message):
    await message.answer(
        "🚗 Надішліть інформацію про перевезення."
    )

@dp.message(F.text == "📄 Документи")
async def documents(message: Message):
    await message.answer(
        "📄 Напишіть ваше питання щодо документів."
    )

@dp.message(F.text == "📢 Реклама")
async def ads(message: Message):
    await message.answer(
        "📩 Для реклами звертайтесь:\n@Sovkin25"
    )

# =========================
# МОДЕРАЦІЯ
# =========================

@dp.message()
async def send_to_admin(message: Message):

    user = message.from_user

    text = f"""
📨 <b>Нове оголошення</b>

👤 {user.full_name}
🆔 @{user.username if user.username else 'немає username'}

📝
{message.text}
"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Опублікувати",
                    callback_data=f"publish_{message.message_id}"
                )
            ]
        ]
    )

    await bot.send_message(
        ADMIN_ID,
        text,
        reply_markup=keyboard
    )

    await message.answer(
        "✅ Ваше оголошення відправлено на модерацію."
    )

# =========================
# ПУБЛІКАЦІЯ
# =========================

@dp.callback_query(F.data.startswith("publish"))
async def publish_post(callback: CallbackQuery):

    original_text = callback.message.text

    await bot.send_message(
        CHANNEL_USERNAME,
        f"{original_text}\n\n🇵🇱 @uahubpol"
    )

    await callback.answer("Опубліковано!")
    await callback.message.edit_text(
        callback.message.text + "\n\n✅ ОПУБЛІКОВАНО"
    )

# =========================
# ЗАПУСК
# =========================

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

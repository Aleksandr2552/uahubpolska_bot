from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

from database import add_user

router = Router()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔥 Робота'),
            KeyboardButton(text='🏠 Житло')
        ],
        [
            KeyboardButton(text='🛠 Послуги'),
            KeyboardButton(text='🚗 Перевезення')
        ],
        [
            KeyboardButton(text='📄 Документи'),
            KeyboardButton(text='📢 Реклама')
        ]
    ],
    resize_keyboard=True
)

@router.message(CommandStart())
async def start(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    text = """
🇵🇱 <b>Ласкаво просимо в UA HUB Polska</b>

🔥 Робота
🏠 Житло
🛠 Послуги
🚗 Перевезення
📄 Документи

👇 Оберіть категорію
"""

    await message.answer(
        text,
        reply_markup=main_keyboard
    )
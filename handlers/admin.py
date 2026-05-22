from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
from database import get_stats

router = Router()

@router.message(Command('stats'))
async def stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    users, ads = await get_stats()

    text = f"""
📊 Статистика бота

👥 Користувачів: {users}
📨 Оголошень: {ads}
"""

    await message.answer(text)
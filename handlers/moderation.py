from aiogram import Router
from aiogram import F

from aiogram.types import CallbackQuery

from config import CHANNEL_USERNAME

router = Router()

@router.callback_query(F.data == 'publish')
async def publish(callback: CallbackQuery):

    if callback.message.photo:

        await callback.bot.send_photo(
            CHANNEL_USERNAME,
            callback.message.photo[-1].file_id,
            caption=callback.message.caption
        )

    else:

        await callback.bot.send_message(
            CHANNEL_USERNAME,
            callback.message.text
        )

    await callback.answer('✅ Опубліковано')

@router.callback_query(F.data == 'decline')
async def decline(callback: CallbackQuery):

    await callback.answer('❌ Відхилено')
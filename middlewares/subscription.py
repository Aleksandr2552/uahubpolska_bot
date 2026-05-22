from aiogram import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from config import CHANNEL_USERNAME
from config import CHANNEL_LINK

class SubscriptionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler,
        event,
        data
    ):

        bot = data['bot']

        try:

            member = await bot.get_chat_member(
                CHANNEL_USERNAME,
                event.from_user.id
            )

            subscribed = member.status in [
                'member',
                'administrator',
                'creator'
            ]

        except:

            subscribed = False

        if not subscribed:

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='📢 Підписатися',
                            url=CHANNEL_LINK
                        )
                    ]
                ]
            )

            await event.answer(
                '❌ Спочатку підпишіться на канал',
                reply_markup=keyboard
            )

            return

        return await handler(event, data)
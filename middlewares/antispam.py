from aiogram import BaseMiddleware

BANNED_WORDS = [
    'casino',
    '1xbet',
    'ставки',
    'bet',
    'crypto scam'
]

class AntiSpamMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler,
        event,
        data
    ):

        if hasattr(event, 'text'):

            text = event.text.lower()

            for word in BANNED_WORDS:

                if word in text:

                    await event.answer(
                        '🚫 Заборонений контент'
                    )

                    return

        return await handler(event, data)
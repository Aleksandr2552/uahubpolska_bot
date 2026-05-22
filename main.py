import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN

from database import create_db

from handlers.start import router as start_router
from handlers.categories import router as categories_router
from handlers.moderation import router as moderation_router
from handlers.admin import router as admin_router

from middlewares.subscription import SubscriptionMiddleware
from middlewares.antispam import AntiSpamMiddleware

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

# MIDDLEWARES

dp.message.middleware(
    SubscriptionMiddleware()
)

dp.message.middleware(
    AntiSpamMiddleware()
)

# ROUTERS

dp.include_router(start_router)
dp.include_router(categories_router)
dp.include_router(moderation_router)
dp.include_router(admin_router)

async def main():

    await create_db()

    print('BOT STARTED')

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
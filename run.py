import asyncio

from aiogram import Bot, Dispatcher
from app.handlers_admin import router_admin
from app.handlers_user import router_user
from app.config import TOKEN, TEST_TOKEN

bot = Bot(token=TEST_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(router_user, router_admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
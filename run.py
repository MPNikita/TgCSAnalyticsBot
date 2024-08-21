import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers_admin import router_admin
from app.handlers_user import router_user
from database.structure import async_main
from dotenv import load_dotenv


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(router_user, router_admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
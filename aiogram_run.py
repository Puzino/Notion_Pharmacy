import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.notion_create_item_callback import callback_notion_add_router
from handlers.notion_del_item_callback import callback_notion_del_upd_router
from handlers.notion_edit_item_callback import callback_notion_edit_router
from handlers.notion_router import notion_router
from handlers.start import start_router
from middleware.access_middleware import AccessMiddleware
from utils.create_bot import bot, dp
from utils.utils import pharmacy_checker

scheduler = AsyncIOScheduler()


async def main() -> None:
    """
    Main func aiogram bot
    :return: None
    """

    dp.include_router(start_router)
    dp.include_router(notion_router)
    dp.include_router(callback_notion_add_router)
    dp.include_router(callback_notion_del_upd_router)
    dp.include_router(callback_notion_edit_router)

    # Middlewares
    dp.message.middleware(AccessMiddleware())

    # Schedule
    scheduler.add_job(pharmacy_checker, "cron", hour=6, minute=0)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

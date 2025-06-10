import asyncio

from handlers.notion_create_item_callback import callback_notion_add_router
from handlers.notion_router import notion_router
from handlers.start import start_router
from utils.create_bot import bot, dp


async def main() -> None:
    """
    Main func aiogram bot
    :return: None
    """

    dp.include_router(start_router)
    dp.include_router(notion_router)
    dp.include_router(callback_notion_add_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

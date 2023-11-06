import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode

from commands import *

load_dotenv()
TOKEN = getenv('TOKEN')

bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)

async def main() -> None:
    print("STARTED:\n")

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
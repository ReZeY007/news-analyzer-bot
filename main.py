import asyncio
import logging
import sys
from dotenv import load_dotenv
load_dotenv()

from bot.bot import bot, dp
from bot.commands import commands


async def main() -> None:
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

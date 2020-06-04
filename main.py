import asyncio
import discord
import traceback
import config
import os

from bot import Bot
from cogs.stand_info import Stands

bot = Bot()
bot.add_cog(Stands(Bot))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.connect_all())
        loop.run_until_complete(bot.start(config.token))
    except Exception as e:
        traceback.print_exc()

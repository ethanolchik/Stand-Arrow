import discord
import asyncpg
import config
import context
from discord.ext import commands

class Bot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(command_prefix='Stand Arrow ', **kwargs)
        self.config = config

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=context.Context)

    async def connect_all(self):
        self.pool = await asyncpg.create_pool(**self.config.db, min_size=10, max_size=20, command_timeout=60.0)

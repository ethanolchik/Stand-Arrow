from discord.ext import commands

class Context(commands.Context):
    """A custom implementation of the command invocation context
       that allows for cross-cutting concerns such as data access"""

    async def get_stand(self, stand_name):
        """Lists all of the relevant information for a particular stand.
           One stand attribute per line of output."""
        return await self.bot.pool.fetchrow(f"SELECT * from stand WHERE stand_name = '{stand_name}'")

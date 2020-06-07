from discord.ext import commands

class Stands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stand_info(self, ctx, stand_name):
        """Lists all of the relevant information for a paritcular stand.
           One stand attribute per line"""
        stand_information = await ctx.get_stand(stand_name)
        await ctx.send("\n".join(str(stand_attribute) for stand_attribute in stand_information))

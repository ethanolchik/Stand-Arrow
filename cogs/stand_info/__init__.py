from discord.ext import commands

class Stands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stand_info(self, ctx, stand_name):
        """Lists all of the relevant information for a paritcular stand.
           One stand attribute per line"""
        stand_information: tuple = await ctx.get_stand(stand_name)
        formatted_message = ("\n".join(str(stand_attribute) for stand_attribute in stand_information))
        if stand_information:
            for chunk in [formatted_message[i:i+2000] for i in range(0, len(formatted_message), 2000)]:
                await ctx.send(chunk)
        #if stand_information:
        #   await ctx.send("\n".join(str(stand_attribute) for stand_attribute in stand_information))
        else:
            await ctx.send(f"There is no stand information available for {stand_name}")
	

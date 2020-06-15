from discord.ext import commands
import utils.model as model


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_inv(self, ctx):
        author = str(ctx.author)
        player_id = await ctx.get_player_id_from_name(author)
        inventory: model.Inventory = await ctx.get_player_inventory(player_id)
        formatted_string = f'{ctx.author} Inventory:\n\n'
        for item, amt in inventory.show_inventory().items():
            formatted_string += f'{item}: {amt}\n'
        await ctx.send(formatted_string)

from discord.ext import commands


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def who(self, ctx):
        author = ctx.author
        await ctx.send(f"Hello {author}")

    @commands.command()
    async def debug_free_cash(self, ctx):
        author = ctx.author
        if str(ctx.author) != "TestUser#0001":
            raise ValueError("Unauthorized API usage")
            await ctx.send("You are not authorized to do that")
        else:
            await ctx.insert_into_inventory(author, "money", 1000)
            await ctx.send("You have been given $1000!")

    @commands.command()
    async def debug_clear(self, ctx):
        author = ctx.author
        if str(ctx.author) != "TestUser#0001":
            raise ValueError("Unauthorized API usage")
            await ctx.send("You are not authorized to do that!")
        else:
            await ctx.clear_inventory(author)

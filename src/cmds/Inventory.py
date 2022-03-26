from discord.ext import commands


class Inventory(commands.Cog):

    CMD = "inventory"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=CMD)
    async def list(self, ctx):
        await ctx.send(f"<@{ctx.author.id}>'s inventory: ...")


if __name__ == "__main__":
    pass

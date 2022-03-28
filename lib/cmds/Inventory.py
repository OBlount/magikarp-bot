from discord.ext import commands
from lib.db.databasemgmt import DbOperations

class Inventory(commands.Cog):

    CMD = "inventory"

    def __init__(self, bot):
        self.bot = bot
        self.operator = DbOperations()

    @commands.command(name=CMD)
    async def list(self, ctx):
        data = self.operator.inventory_read()
        message = f"<@{ctx.author.id}>'s inventory:\n"

        for item in data:
            message = message + str(item[0]) + ": " + str(item[1]) + "\n"

        await ctx.send(message)


if __name__ == "__main__":
    pass

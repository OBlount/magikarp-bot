from lib.cmds import OPERATOR
from discord.ext import commands


class Inventory(commands.Cog):

    CMD = "inventory"

    def __init__(self, bot):
        self.bot = bot

    # An async method which promises a message back to the user when the cmd is
    # struck. It lists out the item_name and item_quanity of each item a
    # trainer owns stored in the db.
    # DOCUMENTATION:
    # string name = CMD
    @commands.command(name=CMD)
    async def list_inventory(self, ctx):
        data = OPERATOR.inventory_read(ctx.author.id)
        message = f"<@{ctx.author.id}>'s inventory:\n"

        for item in data:
            message = message + str(item[0]) + ": " + str(item[1]) + "\n"

        await ctx.send(message)


if __name__ == "__main__":
    pass

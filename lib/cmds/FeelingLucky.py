import random

from lib.cmds import OPERATOR
from discord.ext import commands


class Feeling_Lucky(commands.Cog):

    CMD = "feelinglucky"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=CMD)
    async def fl(self, ctx):
        rand = random.randint(1, 3)

        match rand:
            case 1:
                message = rand
            case 2:
                message = rand
            case 3:
                message = rand

        await ctx.send(message)


if __name__ == "__main__":
    pass

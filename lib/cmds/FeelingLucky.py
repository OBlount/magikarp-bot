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
            # Item Event - Add an item to the player's inventory
            case 1:
                item_name, quantity = self.__give_item(ctx.author.id)
                message = f"<@{ctx.author.id}> got {quantity} {item_name}(s)!\n"
            case 2:
                message = rand
            case 3:
                message = rand

        await ctx.send(message)

    def __give_item(self, trainer_id):
        number_of_items = OPERATOR.get_max_item()
        random_id = random.randint(1, number_of_items)
        random_quantity = random.randint(1, 3)

        val = (trainer_id, random_id, random_quantity)
        OPERATOR.edit_inventory(val)

        return (OPERATOR.get_item_name_from_id(random_id), random_quantity)


if __name__ == "__main__":
    pass

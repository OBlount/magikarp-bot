from discord.ext import commands
from discord.ext.commands import has_permissions

from lib.db.asyncdb import get_all_trainers, register_trainer


class Administrative(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tl")
    @has_permissions(administrator=True)
    async def list_all_trainers(self, ctx):
        data = await get_all_trainers()
        message = ""
        await ctx.send("Trainers:")
        for i in data:
            message = message + str(i[0]) + ", " + str(i[1]) + "\n"
        await ctx.send(message)

    @commands.command(name="register")
    async def register_trainer(self, ctx):
        name = ctx.author.name
        id = ctx.author.id
        values = (id, name)
        if await register_trainer(values):
            await ctx.send(f"User <@{ctx.author.id}> has been registered as a trainer!")
        else:
            await ctx.send(f"Unfortunately, an error has occurred and we have been unable to register user <@{ctx.author.id}>."
                     f"Please contact a server administrator for assistance")



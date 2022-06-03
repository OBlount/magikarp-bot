from discord.ext import commands
from discord.ext.commands import has_permissions

from lib.db.asyncdb import get_all_trainers, register_trainer


class Administrative(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # An async method which promises a message back to the user when the cmd is
    # struck. This queries the db for all trainers registered and lists them out.
    # Only administrators of the server can use this command.
    # DOCUMENTATION:
    # string name = "tl"
    @commands.command(name="tl")
    @has_permissions(administrator=True)
    async def list_all_trainers(self, ctx):
        message = ""
        data = await get_all_trainers()
        for i in data:
            message = message + str(i[0]) + ", " + str(i[1]) + "\n"
        await ctx.send("Trainers:")
        await ctx.send(message)

    # An async method which promises a message back to the user when the cmd is
    # struck. This appends to the db table 'trainers' a new trainer.
    # DOCUMENTATION:
    # string name = "register"
    @commands.command(name="register")
    async def register_trainer(self, ctx):
        name = ctx.author.name
        authorID = ctx.author.id
        values = (authorID, name)
        if await register_trainer(values):
            await ctx.send(f"User <@{ctx.author.authorID}> has been registered as a trainer!")
        else:
            await ctx.send(f"Unfortunately, an error has occurred and we have been unable to register user <@{ctx.author.authorID}>."
                     f"Please contact a server administrator for assistance")


if __name__ == "__main__":
    pass

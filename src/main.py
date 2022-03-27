import os

import discord.errors
from discord.ext import commands
from dotenv import load_dotenv
from cmds.Inventory import Inventory


def createBot():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Inventory(bot))

    return bot


def runBot(bot):
    load_dotenv()
    SESSION_TOKEN = os.getenv("SESSION_TOKEN")

    if SESSION_TOKEN is None:
        print("[ERROR] Please provide your SESSION_TOKEN in a .env\n\rExiting...")
        exit(1)

    try:
        print("Spinning up bot...")
        bot.run(SESSION_TOKEN)
    except discord.errors.LoginFailure as err:
        print(err)
        exit()



if __name__ == "__main__":
    karpBot = createBot()
    runBot(karpBot)

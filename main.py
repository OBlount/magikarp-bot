import os

import discord.errors
from discord.ext import commands
from dotenv import load_dotenv
from lib.cmds.Inventory import Inventory


def create_bot():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Inventory(bot))

    return bot

def run_bot(bot):
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if BOT_TOKEN is None:
        print("[ERROR] Please provide your BOT_TOKEN in a .env\n\rExiting...")
        exit(10)

    try:
        print("Spinning up bot...")
        bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure as err:
        print(err)
        exit()


if __name__ == "__main__":
    karpBot = create_bot()
    run_bot(karpBot)

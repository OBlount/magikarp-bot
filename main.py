import os
import discord.errors

from discord.ext import commands
from dotenv import load_dotenv

from lib.cmds.inventory import Inventory
from lib.cmds.feeling_lucky import FeelingLucky

# A method that adds the cmd prefix and cmd cogs in one go.
# DOCUMENTATION:
# RETURNS:
# bot dicord_bot
def create_bot():
    bot = commands.Bot(command_prefix='!')

    bot.add_cog(Inventory(bot))
    bot.add_cog(FeelingLucky(bot))

    return bot


# A method that first grabs the bot token from the .env file, and then
# tries to spin using bot.run(TOKEN).
# DOCUMENTATION:
# bot bot
def run_bot(bot):
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if BOT_TOKEN is None:
        print("[ERROR] Please provide your BOT_TOKEN in a .env\n\rExiting...")
        exit(10)  # 10 = No bot token provided

    try:
        print("Spinning up bot...")
        bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure as err:
        print(err)
        exit()


if __name__ == "__main__":
    karpBot = create_bot()
    run_bot(karpBot)

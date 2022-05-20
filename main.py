import os
import discord.errors

from discord.ext import commands
from dotenv import load_dotenv

from lib.db.database_maker import create_database
from lib.cmds.inventory import Inventory
from lib.cmds.feeling_lucky import FeelingLucky


# A method that adds the cmd prefix and cmd cogs in one go.
# DOCUMENTATION:
# RETURNS:
# bot discord_bot
def create_bot():
    discord_bot = commands.Bot(command_prefix='!')

    discord_bot.add_cog(Inventory(discord_bot))
    discord_bot.add_cog(FeelingLucky(discord_bot))

    return discord_bot


# A method that first creates the database, then grabs the
# bot token from the .env file, and then tries to
# spin using bot.run(TOKEN).
# DOCUMENTATION:
# bot discord_bot
def run_bot(discord_bot):
    create_database()
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if BOT_TOKEN is None:
        print("[ERROR] Please provide your BOT_TOKEN in a .env\n\rExiting...")
        exit(10)  # 10 = Bot token not provided

    try:
        print("[BOT] Spinning up bot...")
        discord_bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure as err:
        print(err)
        exit()
    except KeyboardInterrupt:
        print("Exiting bot...")


if __name__ == "__main__":
    karpBot = create_bot()
    run_bot(karpBot)

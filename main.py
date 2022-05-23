import os
import discord.errors

from discord.ext import commands
from dotenv import load_dotenv

from lib.cmds.inventory import Inventory
from lib.cmds.feeling_lucky import FeelingLucky
from lib.db.database_maker import CreateDatabase

# A method that adds the cmd prefix and cmd cogs in one go.
# DOCUMENTATION:
# RETURNS:
# bot discord_bot
def create_bot():
    discord_bot = commands.Bot(command_prefix='!')

    discord_bot.add_cog(Inventory(discord_bot))
    discord_bot.add_cog(FeelingLucky(discord_bot))

    return discord_bot


# A method that first grabs the bot token from the .env file, and then
# tries to spin using bot.run(TOKEN).
# DOCUMENTATION:
# bot discord_bot
def run_bot(discord_bot):
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if BOT_TOKEN is None:
        print("[ERROR] Please provide your BOT_TOKEN in a .env\n\r")
        if not os.path.isfile(".env"):
            with open(".env", "w") as env:
                env.write("BOT_TOKEN=BOT_TOKEN_HERE")

        exit(10)  # 10 = Bot token not valid

    try:
        print("[BOT] Spinning up bot...")
        discord_bot.run(BOT_TOKEN)
    except discord.errors.LoginFailure as err:
        print(f"[ERROR] {err}")
        exit(10)
    except KeyboardInterrupt:
        print("Exiting bot...")


if __name__ == "__main__":
    if os.path.abspath(f"{os.curdir}") != os.path.abspath(__file__)[0:-8:1]:
        print("[ERROR] Please start the bot from the same directory as the main.py file.")
        exit()
    CreateDatabase.create_database()
    karpBot = create_bot()
    run_bot(karpBot)

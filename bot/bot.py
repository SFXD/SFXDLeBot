import logging
import os

import discord
from discord.ext import commands

# Environment Variables
BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_PREFIX = os.environ['BOT_PREFIX']

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class SfxdBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX
        )
        self.remove_command('help')
        self.load_extension("utils.errorhandler")
        self.bot_ready = False

    async def on_ready(self):
        print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\n')
        await self.change_presence(activity=discord.Game(name="SFXD LeBot", type=1, url='https://github.com/sfxd'))

        if not self.bot_ready:
            if not bot.get_cog("CogManager"):
                # Load CogManager
                logging.info("Logged in as: {0} (ID: {0.id})\n".format(bot.user))
                logging.info("Loading CogManager")
                self.load_extension("cogs.CogManager")
                cogManager = bot.get_cog("CogManager")
                cogManager._load_extensions()

                self.bot_ready = True


if __name__ == '__main__':
    bot = SfxdBot()
    bot.run(BOT_TOKEN)

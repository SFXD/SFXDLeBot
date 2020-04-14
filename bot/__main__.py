import logging
import os

import discord
from discord.ext import commands

# Load Config
from bot.config import config as BOT_CONFIG


class SfxdBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_CONFIG.PREFIXES
        )
        self.remove_command('help')
        self.load_extension("utils.errorhandler")
        self.bot_ready = False
        self.bot_config = BOT_CONFIG
        # Logging
        self.log = logging.getLogger()
        self.log.setLevel(logging.getLevelName(BOT_CONFIG.LOGGING_LEVEL))
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(handler)

    async def on_ready(self):
        print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\n')
        await self.change_presence(activity=discord.Game(name="SFXD LeBot", type=1, url='https://github.com/sfxd'))

        if not self.bot_ready:
            if not bot.get_cog("CogManager"):
                # Load CogManager
                bot.log.info("Logged in as: {0} (ID: {0.id})\n".format(bot.user))
                bot.log.info("Loading CogManager")
                self.load_extension("cogs.CogManager")
                cog_manager = bot.get_cog("CogManager")
                cog_manager._load_extensions()

                self.bot_ready = True


if __name__ == '__main__':
    bot = SfxdBot()
    bot.run(BOT_CONFIG.TOKEN)

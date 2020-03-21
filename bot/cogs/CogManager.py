import logging
import os

import discord
from discord.ext import commands

# Setup Logging
logger = logging.getLogger()


class CogManager(commands.Cog):
    logger.info("CogManager Loaded")

    def __init__(self, bot):
        self.bot = bot

    def _load_extensions(self):
        # Loads Extensions
        # Bypasses cogmanager
        for fileName in os.listdir("cogs"):
            # Avoid reloading CogManager
            if fileName.lower().endswith(".py") and not (fileName.lower() in ["cogmanager.py"]):
                name = fileName[:-3]
                try:
                    self.bot.load_extension(f"cogs.{name}")
                    logger.info(f'{name} loaded successfully')
                except Exception as error:
                    logger.exception(f'{name} failed to load')

    def _unload_extensions(self):
        # Unloads Extensions
        # Bypasses cogmanager
        for fileName in os.listdir("cogs"):
            # Avoid unloading CogManager
            if fileName.lower().endswith(".py") and not (fileName.lower() in ["cogmanager.py"]):
                name = fileName[:-3]
                try:
                    self.bot.unload_extension(f"cogs.{name}")
                    logger.info(f'{name} unloaded successfully')
                except Exception as error:
                    logger.exception(f'{name} failed to unload')

    @commands.command(name='reloadCogs', aliases=['rc'])
    @commands.is_owner()
    async def reload(self, ctx):
        self._unload_extensions()
        self._load_extensions()
        await ctx.send('Cogs Reloaded')


def setup(bot):
    bot.add_cog(CogManager(bot))

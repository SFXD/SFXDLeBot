import logging
import os

import discord
from discord.ext import commands

class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.log.info("CogManager Loaded")

    def _load_extensions(self):
        # Loads Extensions
        # Bypasses cogmanager
        for fileName in os.listdir("cogs"):
            # Avoid reloading CogManager
            if fileName.lower().endswith(".py") and not (fileName.lower() in ["cogmanager.py"]):
                name = fileName[:-3]
                try:
                    self.bot.load_extension(f"cogs.{name}")
                    self.bot.log.info(f'{name} loaded successfully')
                except Exception as error:
                    self.bot.log.exception(f'{name} failed to load')

    def _unload_extensions(self):
        # Unloads Extensions
        # Bypasses cogmanager
        for fileName in os.listdir("cogs"):
            # Avoid unloading CogManager
            if fileName.lower().endswith(".py") and not (fileName.lower() in ["cogmanager.py"]):
                name = fileName[:-3]
                try:
                    self.bot.unload_extension(f"cogs.{name}")
                    self.bot.log.info(f'{name} unloaded successfully')
                except Exception as error:
                    self.bot.log.exception(f'{name} failed to unload')

    @commands.command(name='reloadCogs', aliases=['rc'])
    @commands.is_owner()
    async def reload_cogs(self, ctx):
        self._unload_extensions()
        self._load_extensions()
        await ctx.send('Cogs Reloaded')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name="reload_cog")
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        # Reloads 1 specific cog
        try:
            self.bot.reload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(CogManager(bot))

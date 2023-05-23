import asyncio
import logging

from aiohttp import ClientSession
import discord
from discord.ext import commands

# Load Config
from bot.config import config as BOT_CONFIG


class SfxdBot(commands.Bot):
    def __init__(self, *args, web_client: ClientSession, **kwargs):
        super().__init__(*args, **kwargs)
        self.web_client = web_client

    async def setup_hook(self) -> None:
        self.remove_command('help')
        await self.load_extension("utils.errorhandler")
        self.bot_ready = False
        self.bot_config = BOT_CONFIG

        # Logging
        self.log = logging.getLogger()
        self.log.setLevel(logging.getLevelName(BOT_CONFIG.LOGGING_LEVEL))
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(handler)

        # Load CogManager
        self.log.info("Loading CogManager")
        await self.load_extension("cogs.CogManager")
        cog_manager = self.get_cog("CogManager")
        await cog_manager._load_extensions()

    async def on_ready(self):
        print(f'\nSuccessfully logged in as: {self.user.name}\nVersion: {discord.__version__}\n')
        await self.change_presence(activity=discord.Game(name="SFXD LeBot", type=1, url='https://github.com/sfxd'))

    async def run(self, token):
        await self.start(token)
        self.bot_ready = True


async def main():
    async with ClientSession() as our_client:
        async with SfxdBot(command_prefix="$", intents=discord.Intents.all(), web_client=our_client) as bot:
            await bot.run(BOT_CONFIG.TOKEN)


asyncio.run(main())

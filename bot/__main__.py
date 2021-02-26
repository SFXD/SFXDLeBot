import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands

# Load Config
from bot.config import config as BOT_CONFIG


class SfxdBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_CONFIG.PREFIXES,
            case_insensitive=True
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

        # Session
        async def create_aiohttp_session():
            self.session = aiohttp.ClientSession(loop=self.loop)

        self.loop.run_until_complete(create_aiohttp_session())

        # Load CogManager
        self.log.info("Loading CogManager")
        self.load_extension("cogs.CogManager")
        cog_manager = self.get_cog("CogManager")
        cog_manager._load_extensions()

    async def on_ready(self):
        print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\n')
        await self.change_presence(activity=discord.Game(name="SFXD LeBot", type=1, url='https://github.com/sfxd'))

    def run(self, token):
        try:
            self.loop.run_until_complete(self.start(token))
            self.bot_ready = True
        except KeyboardInterrupt:
            self.log.info('Exiting')
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
                self.log.info(f"Cancelled task: {task._coro}")

            self.log.info('Logging out!')
            self.loop.run_until_complete(self.logout())

        finally:
            self.loop.run_until_complete(self.session.close())
            self.loop.close()


if __name__ == '__main__':
    bot = SfxdBot()
    bot.run(BOT_CONFIG.TOKEN)

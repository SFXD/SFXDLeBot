import re

import discord
from discord.ext import commands


class Gearset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gearset_re = re.compile(r"(?i)gearset")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.gearset_re.search(message.content):
            await message.add_reaction("<:gearset:469217819213430792>")


def setup(bot):
    bot.add_cog(Gearset(bot))

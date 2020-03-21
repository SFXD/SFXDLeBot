import datetime

import discord
from discord.ext import commands


# Defining the Class
class func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def EMaker(self, title, description, footer):  # Simple Embedded Message Generator
        embed = discord.Embed(
            title=title,
            description=description,
            colour=0x9bf442,  # HEX Colour with 0x at the start
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text=footer)

        return embed

        # To use: (embed=func.EMaker(title, description, footer))


def setup(client):
    client.add_cog(func(client))
# Adding it as a Cog

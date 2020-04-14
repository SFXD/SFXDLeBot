import random

import discord
from discord.ext import commands
import aiohttp

from utils.functions import func


class Birb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="birb")
    async def _birb(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://birb.henry.fail/api") as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(title="Random Birb!",
                                       color=discord.Color.dark_green())
                    em.set_image(url=js["url"])
                    await ctx.send(embed=em)
                else:
                    await ctx.send(embed=func.EMaker(self, "Oops!",
                                                     "Couldn't reach birb.henry.fail.\nTry again later.",
                                                     "Error"))

    @commands.command(name="rbirb")
    @commands.is_owner()
    async def _rbirb(self, ctx):
        headers = {'Authorization': 'Client-ID {}'.format(self.bot.bot_config.IMGUR_TOKEN)}
        url = f"https://api.imgur.com/3/gallery/t/birb"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                if r.status == 200:
                    js = await r.json()

                    imgurItem = random.choice(js["data"]["items"])

                    await ctx.send(imgurItem['link'])
                else:
                    await ctx.send(embed=func.EMaker(self, "Oops!",
                                                     f"Couldn't reach imgur.\nTry using {ctx.prefix}birb instead",
                                                     "Error"))


def setup(client):
    client.add_cog(Birb(client))

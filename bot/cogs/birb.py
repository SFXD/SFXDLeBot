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


def setup(client):
    client.add_cog(Birb(client))

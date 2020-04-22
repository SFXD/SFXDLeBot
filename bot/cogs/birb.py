import random
import time

import discord
from discord.ext import commands

from utils.functions import func


class Birb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birbImgurCache = None
        self.birbImgurCacheTime = None

    @commands.command(name="obirb")
    async def _birb(self, ctx):
        async with self.bot.session.get("https://birb.henry.fail/api") as r:
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

    async def _getimgurgallery(self, tag):
        headers = {'Authorization': 'Client-ID {}'.format(self.bot.bot_config.IMGUR_TOKEN)}
        url = f"https://api.imgur.com/3/gallery/t/{tag}"
        async with self.bot.session.get(url, headers=headers) as r:
            if r.status == 200:
                return await r.json()

    @commands.command(name="birb")
    async def _rbirb(self, ctx):
        if (self.birbImgurCache is None) or (time.time() - self.birbImgurCacheTime > 43200):
            js = await self._getimgurgallery('birb')
            self.birbImgurCache = js
            self.birbImgurCacheTime = time.time()
        else:
            js = self.birbImgurCache
        print(len(js["data"]["items"]))
        imgurItem = random.choice(js["data"]["items"])
        await ctx.send(imgurItem['link'])

    @commands.command(name="birbclearcache")
    @commands.is_owner()
    async def _rbirbCacheClear(self, ctx):
        js = await self._getimgurgallery('birb')
        self.birbImgurCache = js
        self.birbImgurCacheTime = time.time()
        self.bot.log.info('Birb Cache Cleared')
        await ctx.send('**`SUCCESS`**')


def setup(client):
    client.add_cog(Birb(client))

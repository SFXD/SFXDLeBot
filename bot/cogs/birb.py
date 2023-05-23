import random
import time

import discord
from discord.ext import commands


class Birb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birbImgurCache = None
        self.birbImgurCacheTime = None

    async def _getimgurgallery(self, tag, sort, window, page):
        headers = {'Authorization': 'Client-ID {}'.format(self.bot.bot_config.IMGUR_TOKEN)}
        url = f"https://api.imgur.com/3/gallery/t/{tag}/{sort}/{window}/{page}"
        async with self.bot.web_client.get(url, headers=headers) as r:
            if r.status == 200:
                return await r.json()

    @commands.command(name="birb")
    async def _rbirb(self, ctx):
        await ctx.channel.typing()
        if (self.birbImgurCache is None) or (time.time() - self.birbImgurCacheTime > 43200):
            print('cache is ded')
            items = []
            for pageNumber in range(1, 4):
                js = await self._getimgurgallery('birb', 'time', 'all', pageNumber)
                items.extend(js["data"]["items"])

                self.birbImgurCache = items
                self.birbImgurCacheTime = time.time()

        # Grab Cache
        js = self.birbImgurCache
        # Randomize Imgur items
        imgurItem = random.choice(js)

        # Check if Gallery
        if imgurItem['in_gallery']:
            galleryImages = random.choice(imgurItem['images'])
            sendItem = galleryImages
        else:
            sendItem = imgurItem

        if sendItem['type'] == 'video/mp4':
            try:
                await ctx.send(sendItem['mp4'])
            except:
                await ctx.send("The birb didn't make it, sorry :no_entry:")

        else:
            link = sendItem['link']

            embed = discord.Embed(title="Here's a birb 🐦", color=discord.Color.random())
            embed.set_image(url=link)
            embed.set_footer(text=link)
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.send("The birb didn't make it, sorry :no_entry:")

    @commands.command(name="abirb")
    async def _abirb(self, ctx):
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "http://random.birb.pw/tweet.json"
        async with self.bot.web_client.get(url, headers=headers) as r:
            if r.status == 200:
                j = await r.json()
                # insert image filename into URL
                url = "http://random.birb.pw/img/{}".format(j["file"])
                embed = discord.Embed(title="Here's a another birb 🐦", color=discord.Color.random())
                embed.set_image(url=url)
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.send("The birb didn't make it, sorry :no_entry:")

    @commands.command(name="birbclearcache")
    @commands.is_owner()
    async def _rbirbCacheClear(self, ctx):
        js = await self._getimgurgallery('birb')
        self.birbImgurCache = js
        self.birbImgurCacheTime = time.time()
        self.bot.log.info('Birb Cache Cleared')
        await ctx.send('**`SUCCESS`**')


async def setup(client):
    await client.add_cog(Birb(client))

import os
import io
import typing

import discord
from discord.ext import commands
import validators


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_image(self, ctx, user_url: typing.Union[discord.Member, str] = None):
        if user_url is None and not ctx.message.attachments:
            async for m in ctx.channel.history(limit=10, before=ctx.message):
                if m.embeds:
                    img = m.embeds[0].image.url
                    if img is not discord.Embed.Empty:
                        break
                if m.attachments:
                    img = m.attachments[0].url
                    break
            else:
                # * If it didn't find an image to use
                img = ctx.author.avatar_url_as(format="png")
        elif ctx.message.attachments:
            img = ctx.message.attachments[0].url
        elif user_url is not None:
            if isinstance(user_url, discord.Member):
                img = user_url.avatar_url_as(format="png")
            elif validators.url(user_url):
                img = user_url
            else:
                raise commands.BadArgument
        return str(img)

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                            "this: `<prefix> america (OPTIONAL)<@mention user OR attach an image OR "
                            "image url>`")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def murica(self, ctx, member_url: typing.Union[discord.Member, str] = None):
        """Overlay the American flag over an image"""

        async with ctx.channel.typing():
            img = await self.get_image(ctx, member_url)
            headers = {'avatars': img}
            async with self.bot.web_client.get("https://imgen.herokuapp.com/america", headers=headers) as resp:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.gif'))

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                            "this: `<prefix> comrade (OPTIONAL)<@mention user OR attach an image OR "
                            "image url>`")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def comrade(self, ctx, member_url: discord.Member = None):
        """Overlay the Russian flag over an image"""

        async with ctx.channel.typing():
            img = await self.get_image(ctx, member_url)
            headers = {'avatars': img}
            async with self.bot.web_client.get("https://imgen.herokuapp.com/communism", headers=headers) as resp:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.gif'))

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                            "this: `<prefix> changemymind <text>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def changemymind(self, ctx, *changeMyMind: str):
        """Change My Mind Memer"""

        async with ctx.channel.typing():
            headers = {'text': changeMyMind}
            async with self.bot.web_client.get("https://imgen.herokuapp.com/changemymind", headers=headers) as resp:
                print(resp)
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.png'))

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                            "this: `<prefix> dabme <text>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dabme(self, ctx, user: discord.Member = None):
        """Dab Memer"""

        async with ctx.channel.typing():
            img = await self.get_image(ctx, user)
            headers = {'avatars': img}
            async with self.bot.web_client.get("https://imgen.herokuapp.com/dab", headers=headers) as resp:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.png'))

    @commands.command(brief="You didn't format the command correctly. It's supposed to look like "
                            "this: `<prefix> doorkicknvm <text>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def doorkicknvm(self, ctx, user: discord.Member = None):
        """doorkicknvm memer"""

        async with ctx.channel.typing():
            img = await self.get_image(ctx, user)
            headers = {'avatars': img}
            async with self.bot.web_client.get("https://imgen.herokuapp.com/door", headers=headers) as resp:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.png'))


async def setup(client):
    await client.add_cog(Image(client))

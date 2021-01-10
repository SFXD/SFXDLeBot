import io
import json

import discord
from discord.ext import commands

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}


class Finvizcrypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="btc")
    async def btc(self, ctx):
        await self.get_crypto(ctx, 'BTCUSD')

    @commands.command(name="eth")
    async def eth(self, ctx):
        await self.get_crypto(ctx, 'ETHUSD')

    async def get_crypto(self, ctx, chart):
        await ctx.trigger_typing()
        async with self.bot.session.get("https://finviz.com/api/crypto_all.ashx?timeframe=m5", headers=headers) as r:
            if r.status == 200:
                jstring = await r.text()
                js = json.loads(jstring)
                data = js[chart]
                changeValue = data['last'] - data['prevClose']
                color = discord.Color.green() if data['change'] >= 0 else discord.Color.red()
                em = discord.Embed(title="{} Price".format(chart), color=color,
                                   url="https://finviz.com/crypto_charts.ashx?p=d1&t={}".format(chart))
                em.add_field(name="USD Price", value=data['last'])
                em.add_field(name="Change %", value=data['change'])
                em.add_field(name="Change", value="{:0.2f}".format(changeValue))
                em.add_field(name="High", value=data['high'])
                em.add_field(name="Low", value=data['low'])
                chart_file = await self.grab_finviz_chart(chart)
                await ctx.send(embed=em, file=chart_file)
            else:
                await ctx.send("Error Retrieving FinViz {} Price".format(chart))

    async def grab_finviz_chart(self, chart):
        async with self.bot.session.get("https://elite.finviz.com/fx_image.ashx?{}_m5_l.png".format(chart),
                                        headers=headers) as r:
            if r.status == 200:
                data = io.BytesIO(await r.read())
                file = discord.File(data, filename="{}5m.png".format(chart))
                return file


def setup(client):
    client.add_cog(Finvizcrypto(client))

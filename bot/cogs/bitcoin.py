import os
import io
import json

import discord
from discord.ext import commands


class Bitcoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="btc")
    async def btc(self, ctx):
        await ctx.trigger_typing()
        async with self.bot.session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as r:
            if r.status == 200:
                jstring = await r.text()
                js = json.loads(jstring)
                value = js['bpi']['USD']['rate']

                em = discord.Embed(title="Bitcoin USD Price", color=discord.Color.green(),
                                   url="https://www.coindesk.com/price/bitcoin")
                em.add_field(name="USD Price", value=value)
                chart_file = await self.grab_btc_chart()
                await ctx.send(embed=em, file=chart_file)
            else:
                await ctx.send("Error Retrieving Coindesk USD/BTC Price")

    async def grab_btc_chart(self):
        async with self.bot.session.get("https://elite.finviz.com/fx_image.ashx?BTCUSD_m5_l.png") as r:
            if r.status == 200:
                data = io.BytesIO(await r.read())
                file = discord.File(data, filename="BTCUSD5m.png")
                return file

def setup(client):
    client.add_cog(Bitcoin(client))

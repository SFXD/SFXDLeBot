import os

import discord
from discord.ext import commands

class Bitcoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="btc")
    async def btc(self, ctx, *location: str):
        await ctx.trigger_typing()
        async with self.bot.session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as r:
            if r.status == 200:
                js = await r.json()
                value = js['bpi']['USD']['rate']
                
                em = discord.Embed(title="Bitcoin USD Price"), color=discord.Color.green(), url="https://www.coindesk.com/price/bitcoin")
                em.add_field(name="USD Price", value=value)
                await ctx.send(embed=em)
            else:
                await ctx.send("Error Retrieving Coindesk USD/BTC Price")
    
def setup(client):
    client.add_cog(Bitcoin(client))

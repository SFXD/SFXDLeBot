import os

import discord
from discord.ext import commands

class Stonk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stonk")
    async def stonk(self, ctx, *ticker: str):
        await ctx.trigger_typing()
        async with self.bot.session.get("https://query1.finance.yahoo.com/v8/finance/chart/{}".format(ticker)) as r:
            if r.status == 200:
                js = await r.json()
                regularMarketPrice = js['chart']['result'][0]['meta']['regularMarketPrice']
                
                em = discord.Embed(title="{} USD Price".format(ticker), color=discord.Color.green(), url="https://finance.yahoo.com/quote/{0}?p={0}".format(ticker))
                em.add_field(name="Current Price", value=regularMarketPrice)
                await ctx.send(embed=em)
            else if r.status == 404:
                await ctx.send("Error quote not found for {}".format(ticker))
            else:
                await ctx.send("Error retrieving quote data for {}. Try again later.".format(ticker))
    
def setup(client):
    client.add_cog(Stonk(client))

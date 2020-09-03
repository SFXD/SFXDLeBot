import discord
from discord.ext import commands

class Stonk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stonk")
    async def stonk(self, ctx, *tickers: str):
        try:
            await ctx.trigger_typing()
            for ticker in tickers:
                embed = await self.build_embed(ticker)
                await ctx.send(embed=embed)
        except Exception as ex:
            self.bot.log.error(ex)

    async def build_embed(self, ticker):
        async with self.bot.session.get("https://query1.finance.yahoo.com/v7/finance/options/{}".format(ticker)) as r:
            embed = None
            if r.status == 200:
                js = await r.json()
                if len(js["optionChain"]["result"]) > 0:
                    embed = self.build_quote_embed(js)
                else:
                    embed = self.build_not_found_embed(ticker)
            elif r.status == 404:
                embed = self.build_not_found_embed(ticker)
            else:
                embed = discord.Embed(title="Error retrieving quote data for {}. Try again later.".format(ticker))
            
            return embed

    def build_not_found_embed(self, ticker):
        return discord.Embed(title="Error quote not found for {}".format(ticker))

    def build_quote_embed(self, js):
        quoteDict = js["optionChain"]["result"][0]["quote"]
        tickerSymbol = quoteDict["symbol"]
        tickerCurrency = quoteDict["currency"]
        longName = quoteDict["longName"]
        fullExchangeName = quoteDict["fullExchangeName"]
        regularMarketPrice = quoteDict["regularMarketPrice"]
        regularMarketChange = round(quoteDict["regularMarketChange"], 2)
        regularMarketChangePercent = round(quoteDict["regularMarketChangePercent"], 2)

        embed = discord.Embed(
            title="{} ({})".format(longName, tickerSymbol),
            color=discord.Color.green(),
            url="https://finance.yahoo.com/quote/{0}?p={0}".format(tickerSymbol),
        )
        # format using diff markdown co we get pretty colors
        if regularMarketChange > 0:
            regularMarketChange = "+{}".format(regularMarketChange)
        if regularMarketChangePercent > 0:
            regularMarketChangePercent = "+{}".format(regularMarketChangePercent)
        embed.add_field(name="Price", value="```diff\n{}```".format(regularMarketPrice), inline=True)
        embed.add_field(name="Change", value="```diff\n{}```".format(regularMarketChange), inline=True)
        embed.add_field(name="Change %", value="```diff\n{}```".format(regularMarketChangePercent), inline=True)
        embed.add_field(name="Exchange", value=fullExchangeName, inline=True)
        embed.add_field(name="Currency", value=tickerCurrency, inline=True)
        return embed

def setup(client):
    client.add_cog(Stonk(client))

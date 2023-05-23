import discord
from discord.ext import commands
from utils.stonkchart import Chart
import io

class Stonk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stonk")
    async def stonk(self, ctx, *tickers: str):
        try:
            if len(tickers) == 0:
                await ctx.send("```\nUsage: $stonk <ticker>\nExample: $stonk TSLA```")
            for ticker in tickers:
                quote_result = await self.build_quote(ctx, ticker)
                if isinstance(quote_result, str):
                    await ctx.send(content=quote_result)
                elif quote_result is None:
                    await ctx.message.add_reaction("👎")
                else:
                    chart_file = await self.build_chart_file(ticker)
                    await ctx.send(embed=quote_result, file=chart_file)
        except Exception as ex:
            self.bot.log.error(ex)
            await ctx.message.add_reaction("👎")

    async def build_quote(self, ctx, ticker):
        async with self.bot.web_client.get("https://query1.finance.yahoo.com/v7/finance/options/{}".format(ticker)) as r:
            if r.status != 200:
                return

            js = await r.json()
            if len(js["optionChain"]["result"]) == 0:
                return

            quote_dict = js["optionChain"]["result"][0]["quote"]
            symbol = quote_dict["symbol"]
            currency = quote_dict["currency"]
            longName = quote_dict["longName"]
            fullExchangeName = quote_dict["fullExchangeName"]
            regularMarketPrice = quote_dict["regularMarketPrice"]
            regularMarketChange = round(quote_dict["regularMarketChange"], 2)
            regularMarketChangePercent = round(quote_dict["regularMarketChangePercent"], 2)

            # format using diff markdown co we get pretty colors
            if regularMarketChange > 0:
                regularMarketChange = "+{}".format(regularMarketChange)
                color = discord.Color.green()
                regularMarketChangePercent = "+{}".format(regularMarketChangePercent)
            else:
                color = discord.Color.red()

            result = discord.Embed(
                title="{} ({})".format(longName, symbol),
                color=color,
                url="https://finance.yahoo.com/quote/{0}?p={0}".format(symbol),
            )
            result.add_field(name="Price", value="```diff\n{}```".format(regularMarketPrice), inline=True)
            result.add_field(name="Change", value="```diff\n{}```".format(regularMarketChange), inline=True)
            result.add_field(name="Change %", value="```diff\n{}```".format(regularMarketChangePercent), inline=True)
            result.add_field(name="Exchange", value=fullExchangeName, inline=True)
            result.add_field(name="Currency", value=currency, inline=True)
            return result
        
    async def build_chart_file(self, ticker):
        async with self.bot.web_client.get("https://query1.finance.yahoo.com/v7/finance/chart/{}".format(ticker)) as r:
            if r.status == 200:
                js = await r.json()
                if len(js["chart"]["result"][0]["indicators"]["quote"][0]) == 0:
                    return
                
                quotes = js["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                previousClose = js["chart"]["result"][0]["meta"]["previousClose"]

                png_bytes = Chart(quotes, previousClose, scale=2).draw_chart()
                file = discord.File(io.BytesIO(initial_bytes=png_bytes), filename="test.png")
                return file


async def setup(client):
    await client.add_cog(Stonk(client))

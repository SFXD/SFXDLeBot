import drawSvg as draw
import discord
from discord.ext import commands
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
        async with self.bot.session.get("https://query1.finance.yahoo.com/v7/finance/options/{}".format(ticker)) as r:
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
        async with self.bot.session.get("https://query1.finance.yahoo.com/v7/finance/chart/{}".format(ticker)) as r:
            if r.status == 200:
                js = await r.json()
                if len(js["chart"]["result"][0]["indicators"]["quote"][0]) == 0:
                    return
                
                quotes = js["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                previousClose = js["chart"]["result"][0]["meta"]["previousClose"]

                # get quote stats
                num_quotes = len(quotes)
                max_quote = previousClose
                min_quote = previousClose
                for quote in quotes:
                    if quote is not None and quote > max_quote:
                        max_quote = quote
                    if quote is not None and quote < min_quote:
                        min_quote = quote

                # settings for chart dimensions and spacing
                scale = 4
                chart_width = max(388, num_quotes-1) * scale
                chart_height = 150 * scale
                chart_padding_top = 10 * scale
                chart_padding_bottom = 10 * scale
                chart_margin_top = 30 * scale
                chart_margin_right = 70 * scale
                chart_margin_bottom = 0 * scale
                chart_margin_left = 0 * scale

                # Create a canvas for the chart
                canvas = draw.Drawing(
                    chart_width + chart_margin_right + chart_margin_left,
                    chart_height + chart_padding_top + chart_padding_bottom + chart_margin_top + chart_margin_bottom,
                    displayInline=False)

                # create a chart using a polygon
                chart_ratio = (max_quote - min_quote) / chart_height
                step_x = scale
                start_x = chart_margin_left
                start_y = chart_margin_bottom
                offset_y = chart_margin_bottom + chart_padding_bottom
                end_x = start_x + (num_quotes-1) * step_x
                end_y = start_y
                previous_close_y = ((previousClose - min_quote) / chart_ratio) + offset_y
                last_y = ((quotes[num_quotes - 1] - min_quote) / chart_ratio) + offset_y

                # create chart points
                points = []
                next_x = start_x - step_x
                next_y = None
                for idx in range(num_quotes):
                    point = quotes[idx]
                    if point is not None:
                        next_y = ((point - min_quote) / chart_ratio) + offset_y
                    next_x += step_x
                    points.append(next_x)
                    points.append(next_y)
                points.append(end_x)
                points.append(end_y)

                # chart color
                chart_fill = "rgba({green_rgb},0.5)".format_map({"green_rgb": "0,135,60"})
                if (previous_close_y > last_y):
                    chart_fill = "rgba({red_rgb},0.5)".format_map({"red_rgb": "240,22,47"})

                # draw chart with white background
                canvas.append(draw.Rectangle(
                    start_x, chart_margin_bottom,
                    chart_width, chart_height + chart_padding_top + chart_padding_bottom,
                    fill="white"))
                canvas.append(draw.Lines(
                    chart_margin_left, chart_margin_bottom, *points,
                    close=True, fill=chart_fill, stroke="black"))

                # settings for creating tags and lines
                sig_figs = len(str(round(max_quote)))
                width_char = 14 * scale
                font_size = 14 * scale
                width_nubbin = width_char
                width_rect = (width_char * (sig_figs + 2))
                height_rect = 22 * scale
                chart_boundary_x = start_x + chart_width

                # create tag for previous close
                prev_close_value = str(round(previousClose, 2))
                prev_close_tag = self.create_chart_tag(prev_close_value, font_size,
                                                       start_x, chart_boundary_x, previous_close_y, width_nubbin,
                                                       width_rect, height_rect, "grey")
                for el in prev_close_tag:
                    canvas.append(el)

                # create tag for current close
                curr_close_value = str(round(quotes[num_quotes - 1], 2))
                curr_close_tag = self.create_chart_tag(curr_close_value, font_size,
                                                       start_x, chart_boundary_x, last_y, width_nubbin,
                                                       width_rect, height_rect, chart_fill)
                for el in curr_close_tag:
                    canvas.append(el)

                # convert svg to png
                png_bytes = canvas.rasterize().pngData
                
                file = discord.File(io.BytesIO(initial_bytes=png_bytes), filename="test.png")
                return file

    def create_chart_tag(self, value, font_size, start_x, end_x, start_y, width_nubbin, width_rect, height_rect, fill_color):
        chart_line = draw.Line(start_x, start_y,
                               end_x, start_y,
                               stroke="black")
        tag_rect = draw.Lines(end_x, start_y,
                              end_x + width_nubbin, start_y + height_rect / 2,
                              end_x + width_nubbin + width_rect, start_y + height_rect / 2,
                              end_x + width_nubbin + width_rect, start_y - height_rect / 2,
                              end_x + width_nubbin, start_y - height_rect / 2,
                              close=True, fill=fill_color)
        tag_text = draw.Text(value, font_size,
                             end_x + width_nubbin, start_y - font_size * 0.3,
                             fill="white", font_family="monospace", font_weight="bold")
        return [chart_line, tag_rect, tag_text]

def setup(client):
    client.add_cog(Stonk(client))

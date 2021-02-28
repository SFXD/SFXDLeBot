import os

import discord
from discord.ext import commands

from utils.functions import func


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="weather")
    async def weather(self, ctx, *location: str):
        if len(location) > 0:
            await ctx.trigger_typing()
            if len(location[0]) == 5 and str(location[0]).isdigit():
                payload = {'zip': location[0], 'appid': self.bot.bot_config.OWM_TOKEN}
            else:
                payload = {'q': " ".join(location), 'appid': self.bot.bot_config.OWM_TOKEN}

            headers = {'user-agent': 'sfxdbot'}
            url = 'http://api.openweathermap.org/data/2.5/weather?'
            async with self.bot.session.get(url, params=payload, headers=headers) as r:
                if r.status == 200:
                    weather_response = await r.json()
                    icon = weather_response['weather'][0]['icon']
                    name = weather_response['name'] + ', ' + weather_response['sys']['country']
                    city_id = weather_response['id']
                    em = discord.Embed(title='Weather in {}'.format(name), color=discord.Color.blue(),
                                       description=weather_response['weather'][0]['description'],
                                       url='https://openweathermap.org/city/{}'.format(city_id))
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    em.set_thumbnail(url='https://openweathermap.org/img/w/{}.png'.format(icon))
                    await ctx.send(embed=em)

                else:
                    await ctx.send(embed=func.EMaker(self, "Oops!",
                                                     "Couldn't reach weather service\nTry again later.",
                                                     "Error"))
        else:
            await ctx.send(embed=func.EMaker(self, "Error!",
                                             f"You can run the command via ```{ctx.prefix}weather <city>```",
                                             "Error"))

    @weather.error
    async def weather_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            await ctx.send(embed=func.EMaker(self, "Error!",
                                             f"Woah woah {ctx.author.mention} calm down, need to wait to run again",
                                             "Error"))


def setup(client):
    client.add_cog(Weather(client))

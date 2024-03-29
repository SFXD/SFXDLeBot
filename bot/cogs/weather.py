import os

import discord
from discord import app_commands
from discord.ext import commands

from utils.functions import func


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="weather", aliases=['w'])
    async def weather(self, ctx, *location: str):
        if len(location) > 0:
            await ctx.channel.typing()
            if len(location[0]) == 5 and str(location[0]).isdigit():
                payload = {'zip': location[0], 'appid': self.bot.bot_config.OWM_TOKEN}
            else:
                payload = {'q': " ".join(location), 'appid': self.bot.bot_config.OWM_TOKEN}

            headers = {'user-agent': 'sfxdbot'}
            url = 'http://api.openweathermap.org/data/2.5/weather?'
            async with self.bot.web_client.get(url, params=payload, headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    celcius = js['main']['temp'] - 273
                    fahrenheit = js['main']['temp'] * 9 / 5 - 459
                    temperature = '{0:.1f} Celsius\n{1:.1f} Fahrenheit'.format(celcius, fahrenheit)
                    humidity = str(js['main']['humidity']) + '%'
                    pressure = str(js['main']['pressure']) + ' hPa'
                    wind_kmh = str(round(js['wind']['speed'] * 3.6)) + ' km/h'
                    wind_mph = str(round(js['wind']['speed'] * 2.23694)) + ' mph'
                    clouds = js['weather'][0]['description'].title()
                    icon = js['weather'][0]['icon']
                    name = js['name'] + ', ' + js['sys']['country']
                    city_id = js['id']
                    em = discord.Embed(title='Weather in {}'.format(name), color=discord.Color.blue(),
                                       description='\a\n')
                    em.add_field(name='**Conditions**', value=clouds)
                    em.add_field(name='**Temperature**', value=temperature)
                    em.add_field(name='\a', value='\a')
                    em.add_field(name='**Wind**', value='{}\n{}'.format(wind_kmh, wind_mph))
                    em.add_field(name='**Pressure**', value=pressure)
                    em.add_field(name='**Humidity**', value=humidity)
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

    @app_commands.command(name="weather", description="Get weather info in your location")
    @app_commands.describe(location="The Zipcode or City you want to get the weather from")
    async def appWeather(self, ctx: discord.Interaction, location: str):
        if len(location[0]) == 5 and str(location[0]).isdigit():
            payload = {'zip': location[0], 'appid': self.bot.bot_config.OWM_TOKEN}
        else:
            payload = {'q': " ".join(location), 'appid': self.bot.bot_config.OWM_TOKEN}

        headers = {'user-agent': 'sfxdbot'}
        url = 'http://api.openweathermap.org/data/2.5/weather?'
        async with self.bot.web_client.get(url, params=payload, headers=headers) as r:
            if r.status == 200:
                js = await r.json()
                celcius = js['main']['temp'] - 273
                fahrenheit = js['main']['temp'] * 9 / 5 - 459
                temperature = '{0:.1f} Celsius\n{1:.1f} Fahrenheit'.format(celcius, fahrenheit)
                humidity = str(js['main']['humidity']) + '%'
                pressure = str(js['main']['pressure']) + ' hPa'
                wind_kmh = str(round(js['wind']['speed'] * 3.6)) + ' km/h'
                wind_mph = str(round(js['wind']['speed'] * 2.23694)) + ' mph'
                clouds = js['weather'][0]['description'].title()
                icon = js['weather'][0]['icon']
                name = js['name'] + ', ' + js['sys']['country']
                city_id = js['id']
                em = discord.Embed(title='Weather in {}'.format(name), color=discord.Color.blue(),
                                   description='\a\n')
                em.add_field(name='**Conditions**', value=clouds)
                em.add_field(name='**Temperature**', value=temperature)
                em.add_field(name='\a', value='\a')
                em.add_field(name='**Wind**', value='{}\n{}'.format(wind_kmh, wind_mph))
                em.add_field(name='**Pressure**', value=pressure)
                em.add_field(name='**Humidity**', value=humidity)
                em.set_thumbnail(url='https://openweathermap.org/img/w/{}.png'.format(icon))
                await ctx.send(embed=em)

            else:
                await ctx.send(embed=func.EMaker(self, "Oops!",
                                                                  "Couldn't reach weather service\nTry again later.",
                                                                  "Error"))


async def setup(client):
    await client.add_cog(Weather(client))

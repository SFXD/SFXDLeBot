import discord
from discord.ext import commands

from utils.functions import func


class Sfstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sfstatus")
    async def _sfStatusCheck(self, ctx, *instance: str):
        if len(instance) == 1:
            await ctx.channel.typing()
            async with self.bot.web_client.get(
                    "https://api.status.salesforce.com/v1/instances/{}/status".format(instance[0])) as r:
                if r.status == 200:
                    js = await r.json()
                    color = discord.Color.green() if js['status'] == "OK" else discord.Color.red()

                    em = discord.Embed(title="Salesforce Instance {} status".format(js['key']),
                                       color=color,
                                       url='https://status.salesforce.com/instances/{}'.format(js['key']))
                    em.add_field(name="Instance Name", value=js['key'])
                    em.add_field(name="Location", value=js['location'])
                    em.add_field(name="Release", value=js['releaseVersion'])
                    em.add_field(name="Status", value=js['status'])
                    await ctx.send(embed=em)
                else:
                    await ctx.send("Couldn't reach status salesforce.\nTry again later.")
        else:
            await ctx.send(embed=func.EMaker(self, "Error!",
                                             f"You can run the command via ```{ctx.prefix}sfstatus <instance id>```",
                                             "Error"))


async def setup(client):
    await client.add_cog(Sfstatus(client))

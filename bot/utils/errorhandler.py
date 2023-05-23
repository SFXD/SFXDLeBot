import discord

from discord.ext import commands
from utils.functions import func


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    For Research on the different exceptions, look here.
    https://discordpy.readthedocs.io/en/latest/api.html#exceptions

    If the error is caused by an import other than discord, you may need to find their Docs instead.
    """

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandOnCooldown, commands.CommandNotFound,
                   commands.NoPrivateMessage, commands.DisabledCommand,
                   discord.NotFound)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.MissingPermissions):
            try:
                return ctx.send(
                    embed=func.EMaker(self, "Error!", "Uh oh.. I seem to be missing some permissions!", "Error"))
            except discord.Forbidden:
                return

        elif isinstance(error, discord.Forbidden):
            try:
                return await ctx.send(embed=func.EMaker(self, "Error!",
                                                        "Uh oh.. I seem to be missing some permissions! Use `!help "
                                                        "permissions` to see what I require!",
                                                        "Error"))
            except discord.Forbidden:
                return

        elif isinstance(error, discord.HTTPException):
            return await ctx.send(
                embed=func.EMaker(self, "Error!", f"There was an error with your command! Here it is: {error}",
                                  "Error"))


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))

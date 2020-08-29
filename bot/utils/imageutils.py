import discord

def find_color(ctx):
    """Find the bot's rendered color. If it's the default color or we're in a DM, return Discord's "blurple" color"""

    try:
        if ctx.guild.me.color == discord.Color.default():
            color = discord.Color.blurple()
        else:
            color = ctx.guild.me.color
    except AttributeError:  #* If it's a DM channel
        color = discord.Color.blurple()
    return color

async def delete_message(ctx, time: float):
    """Deletes a command's message after a certain amount of time"""

    try:
        await ctx.message.delete(delay=time)
    except discord.Forbidden:
        pass
    return


async def send_nekobot_image(ctx, resp):
    """Send an image for a command that called the NekoBot API"""

    if not resp["success"]:
        await ctx.send("Huh, something went wrong. I wasn't able to get the image. Try "
                       "again later", delete_after=5.0)
        return await delete_message(ctx, 5)

    embed = discord.Embed(color=find_color(ctx))
    embed.set_image(url=resp["message"])
    embed.set_footer(text=f"{ctx.command.name} | {ctx.author.display_name}")

    await ctx.send(embed=embed)

async def send_dank_memer_img(ctx, resp, is_gif: bool=False):
    """Send an image for a command that called the Dank Memer Imgen API"""

    def save_image(resp):
        if is_gif:
            filepath = f"{ctx.command.name}-{uuid.uuid4()}.gif"
            with open(filepath, "wb") as f:
                f.write(resp)
        else:
            img = Image.open(io.BytesIO(resp))
            filepath = f"{ctx.command.name}-{uuid.uuid4()}.png"
            img.save(filepath)
        return filepath
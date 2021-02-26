from discord.ext import commands

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="joke")
    async def joke(self, ctx, *category: str):
        # https://github.com/15Dkatz/official_joke_api
        url = 'https://official-joke-api.appspot.com/jokes/'
        if len(category) > 0:
            url += '/'.join([category[0], 'random'])
        else:
            url += 'random'
        self.bot.log.info(url)
        try:
            await ctx.trigger_typing()
            headers = {'user-agent': 'sfxdbot'}
            async with self.bot.session.get(url, headers=headers) as r:
                if r.status == 200:
                    jokeJson = await r.json()
                    if isinstance(jokeJson, list):
                        jokeJson = jokeJson[0]
                    jokeText = '\n'.join([jokeJson['setup'], jokeJson['punchline']])
                    await ctx.send(content=jokeText)
                else:
                    await ctx.send(content='What do you get when the joke server is down?\n' + 
                                   str(r.status) + ' - '+r.reason)
        except Exception as ex:
            self.bot.log.error(ex)
            await ctx.send(content='What do you get when the joke server is down?\n' + str(ex))

def setup(client):
    client.add_cog(Joke(client))

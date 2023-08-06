import discord
from discord.ext import commands
import pynite

class Fortnite:
    '''Example cog for a Discord bot made through the discord.py ext.commands framework.'''

    # Constructor
    def __init__(self, bot):
        self.bot = bot
        self.client = pynite.Client('insert your token here', timeout=5)

    # Create a command
    @commands.command()
    async def profile(self, ctx, platform, name):
        '''Fetch a profile.'''

        player = await self.client.get_player(platform, name)
        solos = await player.get_solos()

        await ctx.send(f"# of kills in solos for {name}: {solos.kills.value}")

def setup(bot):
    bot.add_cog(Fortnite(bot))
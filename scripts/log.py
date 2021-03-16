import discord
from discord.ext import commands


class log(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("log extension loaded")

    
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong {self.client.latency}')


def setup(bot):
    bot.add_cog(log(bot))
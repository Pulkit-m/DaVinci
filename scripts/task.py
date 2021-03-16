import discord
from discord.ext import commands

class task_manager(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Task extension loaded")
    
    async def assign(self, message: discord.Message):
        # await ctx.send("Hello World!!")
        embed = discord.Embed(title = "Task Assigned!")
        text = message.content.split('task-')[1]
        for (i,mem) in enumerate(message.mentions):
            embed.add_field(name = "Student "+str(i+1) , value = mem.mention)
        embed.add_field(name = "Task", value = text)
        embed.add_field(name = "Assigned by: ", value = message.author)
        print(text)
        sent = await message.channel.send(content = None, embed = embed)
        embed_sent = await message.channel.fetch_message(sent.id)
        await embed_sent.add_reaction('\u2611')
        

def setup(bot):
    bot.add_cog(task_manager(bot))
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from scripts.task import task_manager
import pymongo
from pymongo import MongoClient

cluster = MongoClient(os.getenv("CONNECTION_URL"))
db = cluster["year20_21_even_sem"]
students_data = db["students_data"]


load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Bot is ready')
    welcome_channel = bot.get_channel(int(os.getenv('WELCOME_CHANNEL')))
    await welcome_channel.send('Back Online!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("Hi {name}, welcome to Artihc, IIT Jammu's Official discord server.\nPlease register yourself with the official cloud database of our club. \nYou are requested to use your ORIGINAL NAME only for verification purpose. This name will be noted in the database.\nPlease use the following command:\n.register FirstName LastName EntryNumber")
    welcome_channel = bot.get_channel(int(os.getenv('WELCOME_CHANNEL')))
    await welcome_channel.send('{0.name} joined at {0.joined_at}'.format(member))

@bot.event
async def on_message(message):
    if message.author.bot:return
    if message.content == '.stop':
        # await message.channel.send('Turning off bot')
        try:
            await message.reply('Turning off bot')
        finally:
            await bot.logout()

    if message.channel == bot.get_channel(int(os.getenv('TASK_CHANNEL'))) and message.content.startswith('assign'):
        assign_task = bot.get_cog("task_manager")
        await assign_task.assign(message)
        # await message.channel.send(content = None , embed =  embed)

    await bot.process_commands(message)


@bot.event
async def on_raw_message_delete(payload):
    log_channel = bot.get_channel(int(os.getenv('LOG_CHANNEL')))
    try:
        message = payload.cached_message
        embed = discord.Embed(title = "PEEK-A-BOO", description = "A message was deleted!")
        embed.add_field(name = "Sender", value = message.author)
        embed.add_field(name = "Channel", value = message.channel)
        embed.add_field(name = "Content", value = message.content)
        await message.channel.send(content = None, embed = embed)


        # await log_channel.send(message.content)
    except:
        await log_channel.send('deleted message could not be noted down!!')



@bot.event
async def on_raw_reaction_add(payload):
    #payload is short for RawReactionActionEvent
    #channel_id, emoji, event_type, guild_id, member, message_id, user_id
    channel = bot.get_channel(payload.channel_id)
    if channel == bot.get_channel(int(os.getenv("TASK_CHANNEL"))):
        task = await channel.fetch_message(payload.message_id)
        await task.reply('{0.member} reacted to the given task'.format(payload))
        #I will add further functionality after implementing roles and verification database






@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'scripts.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'scripts.{extension}')
    print(f'{extension} unloaded')
    bot.load_extension(f'scripts.{extension}')
    print(f'{extension} loaded')

for cogfile in os.listdir('./scripts'):
    if cogfile.endswith('.py'):
        bot.load_extension(f'scripts.{cogfile[:-3]}')

# print(bot.cogs)


# def assign(message: discord.Message):
#     # await ctx.send("Hello World!!")
#     embed = discord.Embed(title = "Task Assigned!")
#     text = message.content.split('task-')[1]
#     for (i,mem) in enumerate(message.mentions):
#         embed.add_field(name = "Student "+str(i+1) , value = mem.mention)
#     embed.add_field(name = "Task", value = text)
#     embed.add_field(name = "Assigned by: ", value = message.author)
#     print(text)
#     return embed
    


# #just for fun
# @bot.event
# async def on_typing(channel, user, when):
#     await channel.send('{0} kuch to likh raha hai, pata nahi kya dikkat hai isko.'.format(user))

bot.run(os.getenv('TOKEN'))



"""
import random
@bot.command()
async def dankrate(ctx, *, message=None):
    if not message: #nothing is passed after the command
        return await ctx.send("**Please pass in required arguments**")
    message_author = ctx.author
    message_channel = ctx.channel
    
    print(message)
    
    aaaaa = random.randint(1, 101)
    print("{} issued .dankrate 💸".format(message_author))
    
    if aaaaa == 101:
        embedVar = discord.Embed(title="Dank r8 Machine", description=f"you broke the dank machine >:( :fire:\n{message} is {aaaaa}% dank", color=15105570)
    else:
        embedVar = discord.Embed(title="Dank r8 Machine", description=f"{message} is {aaaaa}% dank", color=3066993)
    await message_channel.send(embed=embedVar)


"""
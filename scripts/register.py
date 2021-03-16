import discord
from discord.ext import commands
from discord.ext.commands.core import check
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("SERVER_ID")
cluster = MongoClient(os.getenv("CONNECTION_URL"))
db = cluster["year20_21_even_sem"]
students_data = db["students_data"]

def check_entry_number(entryno):
    year = entryno[:4]
    branch = entryno[5:7]
    no = entryno[7:]
    if (year.isdigit() and branch.isalpha() and no.isdigit()):
        return True
    else: return False



class register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global guild
        print("Registration extension loaded")
        guild = self.bot.get_guild(int(server))

    # async def assign_roles(self, member, entryno):
    #     print(entryno)
    #     if((entryno[4] == 'U' and int(entryno[:4]) > 2016 ) or (entryno[4] == 'P' and int(entryno[:4]) >= 2019 ) or entryno[4] == 'R'):
    #         roles = entryno[:5]+"G"
    #     elif(int(entryno[:4]) <= 2016):
    #         roles = "Alumni"
    #     print(roles)
    #     try:
    #         stu_type = discord.utils.get(guild.roles, name=roles)
    #         await member.add_roles(stu_type)
    #     except:
    #         perms = discord.Permissions(send_messages=False, read_messages=True)
    #         await guild.create_role(name=roles, permissions=perms, mentionable = True)
    #         stu_type = discord.utils.get(guild.roles, name=roles)
    #         await member.add_roles(stu_type)


    @commands.command()
    async def register(self, ctx, name: str = "", entryno : str = ""):
        """
        Use .register FirstName LastName Entry_number to register
        example
        .register Harshit Raj 2019uce0043

        """
        if name!="" and check_entry_number(entryno):
            already_present = students_data.find_one({'_id':entryno})




def setup(bot):
    bot.add_cog(register(bot))
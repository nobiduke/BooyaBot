import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv("TOKEN")
GUILD = int(getenv("GUILD"))

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())


def make_profile(author): # creates db entry for profile
    return {
        "id": str(author.id),
        "display_name": author.display_name,
        "avatar_url": author.avatar.url
    }


@bot.command()
async def alive(ctx): # hello world
    await ctx.send("Its Alive!")


@bot.event
async def on_message(message):

    if message.channel.type == discord.ChannelType.private: # checks dms
        
        if str(message.author.id) not in db["users"]: # if the user doesn't exist than they're profile is updated
            if not isinstance(message.content, str): # error checking
                return
            
            name = " ".join(message.content.split(" ")).lower()

            if name in players.keys() and db_load:

                guild = bot.get_guild(GUILD)
                member = guild.get_member(message.author.id)
                
                await member.edit(nick=name.title())

                if member is None: # quit if member not found
                    return

                db["users"][str(message.author.id)] = {
                    "discord":make_profile(message.author), "data":players[name]
                }

                roleName = "Vet" if players[name]["vet"] == "Vet" else "Rookie"
                
                await member.add_roles(discord.utils.get(guild.roles, name=roleName), reason="They exist!") # adds player role

                await message.channel.send("Welcome!")

    # if the message is a string then checks if its a command and processes
    if isinstance(message.content, str): 
        if message.content[0] == "%":
            await bot.process_commands(message)
    


if __name__== "__main__":
    
    # loads the db. if it breaks then the db functions will turn off with db_load = False
    try:
        db = json.load(open("data/db.json", "r"))
        db_load = True
        print("Database loaded.")
    except FileNotFoundError:
        print("Database failed to load. Care")
        db_load = False

    # loads the players. if it breaks then the db functions will turn off with players_load = False
    try:
        players = json.load(open("data/players.json", "r"))
        print("Players loaded.")
    except FileNotFoundError:
        print("Players failed to load. Care")
        db_load = False

    
    bot.run(TOKEN) # bot starts

    if db_load: # if db was loaded it needs to be saved
        json.dump(db, open("data/db.json", "w"), indent='\t')

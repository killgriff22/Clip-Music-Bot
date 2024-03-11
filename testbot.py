from config import *
import discord 
class User:
    def __init__(self, user):
        self.user: discord.User = user
        self.message_count = 0
    def __repr__(self):
        return self.user
users=[]


swag = discord.Client(intents=discord.Intents.all())

@swag.event
async def on_ready():
    print("What's the deal with airplane food?")

@swag.event
async def on_message(message):
    if message.author == swag.user:
        return
    if "FUCK" in message.content:
       await message.channel.send("HEY! THATS MEAN! >:C")
    #if message author is in users
       #make the user's message counter go up
    #else, add the user to the users list usning User()
    if message.author in users:
        users[users.index(message.author)].message_count += 1
    else:
        users.append(User(message.author))
    if message.content == "dabloon":
)

swag.run(TOKEN)
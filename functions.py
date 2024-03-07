from classes import *


@user.event
async def on_ready():
    print(f'{user.user.name} has connected to Discord!')


@user.event
async def on_message(message):
    if message.author == user.user:
        return
    if not message.channel.id == 1164385876630052945:
        return
    if message.content.startswith('!download'):
        command = message.content.split(' ')
        if "https" in command[1]:
            if "spotify" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(Spotify_path + Spotify.download_url(command[1]))])
            elif "youtube" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(Youtube_path + Youtube.download_url(command[1]))])
            elif "soundcloud" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(Soundcloud_path + Soundcloud.download_url(command[1]))])

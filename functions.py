from classes import *


@user.event
async def on_ready():
    print(f'{user.user.name} has connected to Discord!')

@user.event
async def on_message(message):
    if message.author == user.user:
        return
    if not message.channel.id == 1215317925049667594:
        return
    if message.content.startswith('!download'):
        command = message.content.split(' ')
        if "https" in command[1]:
            if "spotify" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                file = Spotify_path + Spotify.download_url(command[1])
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(file)])
                os.remove(file)
            elif "youtube" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                file = Youtube_path + Youtube.download_url(command[1])
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(file)])
                os.remove(file)
            elif "soundcloud" in command[1]:
                await message.channel.send(f"downloading {command[1]}")
                file = Soundcloud_path + Soundcloud.download_url(command[1])
                await message.channel.send(f"Downloaded {command[1]}",files=[discord.File(file)])
                os.remove(file)
        elif command[1].isdigit():
            for user_ in users:
                if user_.user == message.author:
                    await message.channel.send(f"downloading {user_.search_urls[int(command[1])]}")
                    file = Spotify_path + Spotify.download_url(user_.search_urls[int(command[1])])
                    await message.channel.send(f"Downloaded {user_.search_urls[int(command[1])]}",files=[discord.File(file)])
                    os.remove(file)
        else: #assume we want to search for something
            users.append(User(message.author))
            search = spotify.search(command[1])['tracks']['items']
            users[-1].search_urls = [search[i]['external_urls']['spotify'] for i in range(len(search))]
            await message.channel.send(f"""Search results for {command[1]}\n{"\n".join([f"{i} : {track['name']} - {track['artists'][0]['name']}" for i,track in enumerate(search)])}""")
        
    elif message.content.startswith('!play'):
        if len(queue) == 0:
            command = message.content.split(' ')
            if "https" in command[1]:
                if "youtube" in command[1]:
                    url = command[1]
                    await message.channel.send(f"Playing {url}")
                    author = message.author
                    voice_channel = author.voice_channel
                    vc = await user.join_voice_channel(voice_channel)
                    player = await vc.create_ytdl_player(url)
                    player.start()
"""@tasks.loop(seconds=1)
async def queue_loop():
    if user."""
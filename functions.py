from classes import *


@user.event
async def on_ready():
    print(f'{user.user.name} has connected to Discord!')
    user_prompt_timeout.start()


@user.event
async def on_message(message):
    if message.author == user.user:
        return
    if not message.channel.id == 1215317925049667594:
        return
    if not message.content.startswith('!'):
        return
    split = message.content.split(' ')
    match split[0]:
        case '!download' | '!d':
            command = message.content.split(' ')
            if "https" in command[1]:
                if "spotify" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Spotify_path + Spotify.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
                elif "youtube" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Youtube_path + Youtube.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
                elif "soundcloud" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Soundcloud_path + Soundcloud.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
            elif command[1].isdigit():
                for user_ in users.copy():
                    if user_.user == message.author:
                        await message.channel.send(f"downloading {user_.search_urls[int(command[1])]}")
                        file = Spotify_path + \
                            Spotify.download_url(
                                user_.search_urls[int(command[1])])
                        await message.channel.send(f"Downloaded {user_.search_urls[int(command[1])]}", files=[discord.File(file)])
                        os.remove(file)
                        users.remove(user_)
                        break
            else:  # assume we want to search for something
                users.append(User(message.author))
                search = spotify.search(" ".join(command[1:]))['tracks']['items']
                users[-1].search_urls = [search[i]['external_urls']['spotify']
                                         for i in range(len(search))]
                tracks = [f"{i} : {track['name']} - {track['artists'][0]['name']}" for i, track in enumerate(search)]
                tracks = "\n".join(tracks)
                await message.channel.send(f'Search results for {" ".join(command[1:])}'+"\n"+tracks)
        case '!list' | '!l' | '!album' | '!a' | '!playlist' | '!pl':
            if "https" in split[1]:
                if "spotify" in split[1]:
                    if 'album' in split[1]:
                        users.append(User(message.author))
                        album = spotify.album(split[1].split('/')[-1])
                        for track in album['tracks']['items']:
                            users[-1].search_urls.append(track['external_urls']['spotify'])
                        tracks = [f"{i} : {track['name']} - {track['artists'][0]['name']}" for i, track in enumerate(album['tracks']['items'])]
                        tracks = "\n".join(tracks)
                        await message.channel.send(f'Album {album["name"]}'+"\n"+tracks)
                elif "youtube" in split[1]:
                    await message.channel.send(f"Not Implemented")
                elif "soundcloud" in split[1]:
                    await message.channel.send(f"Not Implemented")
            elif split[1].isdigit():
                for user_ in users.copy():
                    if user_.user == message.author:
                        await message.channel.send(f"downloading {user_.search_urls[int(split[1])]}")
                        file = Spotify_path + \
                            Spotify.download_url(
                                user_.search_urls[int(split[1])])
                        await message.channel.send(f"Downloaded {user_.search_urls[int(split[1])]}", files=[discord.File(file)])
                        os.remove(file)
                        break
        case '!play':
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
@tasks.loop(seconds=1)
async def user_prompt_timeout():
    for user_ in users.copy():
        if user_.timeout > 0:
            user_.timeout -= 1
        else:
            users.remove(user_)
            await user.get_channel(1215317925049667594).send(f"{user_.user.name} timed out")

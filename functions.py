from classes import *
#
#


@user.event
async def on_ready():
    print(f'{user.user.name} has connected to Discord!')
    user_prompt_timeout.start()
    status.start()


@user.event
async def on_message(message: discord.Message):
    if message.author == user.user:
        return
    if message.content.startswith('!'):
        if any(cmd in message.content for cmd in ['!status', '!s']):
            split = message.content.split(' ')
            with open('statuses.txt', 'a') as f:
                add = ' '.join(split[1:])
                f.write(f"{add}\n")
            with open('statuses.txt', 'r') as f:
                length = len(f.readlines())
            await message.channel.send(f"Added {add} to statuses ({length})")
            return
    if not message.channel.id in [1215317925049667594,1164386048407781457]:
        return
    if not message.content.startswith('!'):
        return
    split = message.content.split(' ')
    match split[0]:
        case '!download' | '!d':
            command = message.content.split(' ')
            if "https" in command[1]:  # Given a link
                if "spotify" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Spotify_path + Spotify.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
                elif "youtu" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Youtube_path + Youtube.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
                elif "soundcloud" in command[1]:
                    await message.channel.send(f"downloading {command[1]}")
                    file = Soundcloud_path + \
                        Soundcloud.download_url(command[1])
                    await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                    os.remove(file)
            elif command[1].isdigit():  # Given a number, assume we want to select from a list
                for user_ in users.copy():
                    if user_.user == message.author:
                        url = user_.search_urls[int(command[1])]
                        await message.channel.send(f"downloading {url}")
                        if "spotify" in url:
                            file = Spotify_path + \
                                Spotify.download_url(
                                    user_.search_urls[int(command[1])])
                        elif "youtu" in url:
                            file = Youtube_path + \
                                Youtube.download_url(url)
                        await message.channel.send(f"Downloaded {url}", files=[discord.File(file)])
                        os.remove(file)
                        users.remove(user_)
                        break
            else:  # assume we want to search for something
                users.append(User(message.author))
                search = spotify.search(" ".join(command[1:]))[
                    'tracks']['items']
                # grab the most recent user and append the urls we can download
                users[-1].search_urls = [search[i]['external_urls']['spotify']
                                         for i in range(len(search))]
                # format the search results
                tracks = [f"{i} : {track['name']} - {track['artists'][0]['name']}{f' - album' if 'album' in track['external_urls']['spotify']else f' - playlist' if 'playlist' in track['external_urls']['spotify'] else ''}" for i, track in enumerate(search)]
                tracks = "\n".join(tracks)
                await message.channel.send(f'Search results for {" ".join(command[1:])}'+"\n"+tracks)
        case '!list' | '!l' | '!album' | '!a' | '!playlist' | '!pl':
            if "https" in split[1]:
                if "spotify" in split[1]:
                    if 'album' in split[1]:
                        users.append(User(message.author))
                        album = spotify.album(split[1].split('/')[-1])
                        for track in album['tracks']['items']:
                            users[-1].search_urls.append(
                                track['external_urls']['spotify'])
                        tracks = [f"{i} : {track['name']} - {track['artists'][0]['name']}" for i, track in enumerate(album['tracks']['items'])]
                        tracks = "\n".join(tracks)
                        await message.channel.send(f'Album {album["name"]}'+"\n"+tracks)
                    elif 'playlist' in split[1]:
                        users.append(User(message.author))
                        playlist = spotify.playlist(split[1].split('/')[-1])
                        for track in playlist['tracks']['items']:
                            users[-1].search_urls.append(
                                track['track']['external_urls']['spotify'])
                        tracks = [f"{i} : {track['track']['name']} - {track['track']['artists'][0]['name']}" for i, track in enumerate(playlist['tracks']['items'])]
                        tracks = "\n".join(tracks)
                        await message.channel.send(f'Playlist {playlist["name"]}'+"\n"+tracks)
                elif "youtu" in split[1]:
                    await message.channel.send("Not Implemented")
                    return
                    playlist: Playlist = Playlist(split[1])
                    users.append(User(message.author))
                    for video in playlist.videos:
                        users[-1].search_urls.append(
                            video.watch_url
                        )
                    tracks = [f"{i} : {track.title} - {track.author}" for i,track in enumerate(playlist.videos)]
                    tracks = "\n".join(tracks)
                    await message.channel.send(f'Playlist {playlist.title}'+"\n"+tracks)
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
                        user_.timeout += 10
                        break
        case '!play':
            author = message.author
            voice_channel = message.guild.voice_channels[0]
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="~/.spotdl/ffmpeg",
                    source="Downloads/Spotify/The Living Tombstone - My Ordinary Life.mp3"))


@tasks.loop(seconds=1)
async def user_prompt_timeout():
    for user_ in users.copy():
        if user_.timeout > 0:
            user_.timeout -= 1
        else:
            users.remove(user_)
            await user.get_channel(1215317925049667594).send(f"{user_.user.name} timed out")


@tasks.loop(seconds=20)
async def status():
    with open('statuses.txt', 'r') as f:
        statuses = f.readlines()
        for i, status in enumerate(statuses.copy()):
            statuses[i] = status.strip()
    await user.change_presence(activity=Custom_listening_activity(name=random.choice(statuses)))

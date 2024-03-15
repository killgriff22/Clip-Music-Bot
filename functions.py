from classes import *
#
#
vc: discord.voice_client.VoiceClient | None = None

def update_queue():
    open("queue.txt", "w").write(str(queue))

def read_queue():
    return eval(open("queue.txt").read())

@user.event
async def on_ready():
    global vc
    print(f'{user.user.name} has connected to Discord!')
    user_prompt_timeout.start()
    status.start()
    voice_channel = user.get_guild(1085995033037127750).voice_channels[0]
    vc = await voice_channel.connect()
    queue_loop.start()


@user.event
async def on_message(message: discord.Message):
    global vc, queue, paused, loop
    if message.author == user.user:
        return
    if message.content.startswith('!'):
        for _ in [""]: #allow me to skip this entire chunk of code if i try to stop the queue
            if any(cmd in message.content for cmd in ['!status', '!s']):
                if "!s" in message.content:
                    if any(cmd in message.content for cmd in ['!stop', '!skip']):
                        break
                split = message.content.split(' ')
                with open('statuses.txt', 'a') as f:
                    add = ' '.join(split[1:])
                    f.write(f"{add}\n")
                with open('statuses.txt', 'r') as f:
                    length = len(f.readlines())
                await message.channel.send(f"Added {add} to statuses ({length})")
                return
    if not message.channel.id in [1215317925049667594, 1164386048407781457]:
        return
    if not message.content.startswith('!'):
        return
    split = message.content.split(' ')
    match split[0]:
        case '!download' | '!d':
            command = message.content.split(' ')
            if "https" in command[1]:  # Given a link
                await message.edit(suppress=True)
                msg = await message.channel.send(f"downloading {command[1]}")
                await msg.edit(suppress=True)
                if "spotify" in command[1]:
                    file = Spotify_path + Spotify.download_url(command[1])
                elif "youtu" in command[1]:
                    file = Youtube_path + Youtube.download_url(command[1])
                elif "soundcloud" in command[1]:
                    file = Soundcloud_path + Soundcloud.download_url(command[1])
                msg = await message.channel.send(f"Downloaded {command[1]}", files=[discord.File(file)])
                await msg.edit(suppress=True)
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
                tracks = [f"{i} : {track['name']} - {track['artists'][0]['name']}{f' - album' if 'album' in track['external_urls']['spotify'] else f' - playlist' if 'playlist' in track['external_urls']['spotify'] else ''}" for i, track in enumerate(search)]
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
                    tracks = [f"{i} : {track.title} - {track.author}" for i,
                              track in enumerate(playlist.videos)]
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
        case '!play' | '!p':
            paused = False
            if len(split) >= 2:
                url = split[1]
                command = split
                if "https" in url:
                    subprocess.Popen(["bin/python3", "downloader.py", url])
                elif "cache" in url:
                    await message.channel.send("Not Implemented")
                    return
            elif message.attachments:
                if not any("mp3" in file.filename for file in message.attachments):
                    return
                before_download = set(os.listdir(Discord_path))
                os.chdir(Discord_path)
                for file in message.attachments:
                    if "mp3" in file.filename:
                        if not file.filename in before_download:
                            await file.save(file.filename)
                        else:
                            files.append(file.filename)
                os.chdir(root)
                after_download = set(os.listdir(Discord_path))
                files = list(set(after_download) - set(before_download))
                for i, file in enumerate(files.copy()):
                    files[i] = os.path.join(Discord_path, file)
                queue += files
                update_queue()
            elif paused:
                vc.resume()
                paused = False
        case '!r' | '!remove':
            index = split[1]
            if index.is_digit():
                if int(index) < len(queue):
                    queue.pop(int(index)-1 if int(index)-1 < 0 else int(index))
        case '!queue' | '!q':
            desc = "".join(
                [f"{i}: {file.split('/')[-1].split('.')[0]}\n" for i, file in enumerate(queue)])
            await message.channel.send(
                embed=discord.Embed(
                    title="QUEUE",
                    color=discord.Color.blurple(),
                    description=desc
                )
            )
        case '!pause' | '!paws':
            if not paused:
                vc.pause()
                paused = True
        case '!resume' | '!res':
            if paused:
                vc.resume()
                paused = False
        case '!c' | '!clear' | '!stop' | '!end':
            vc.stop()
            queue = []
            update_queue()
        case '!skip' | '!next':
            vc.stop()
            queue.pop(0)
        case '!loop' | '!l':
            loop = not loop
            await message.reply(f"loop {'on' if loop else 'off'}")
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


@tasks.loop(seconds=1)
async def queue_loop():
    global queue
    queue = read_queue()
    if not queue:
        return
    music_channel = user.get_guild(
        1085995033037127750).get_channel(1164386048407781457)
    while queue:
        await music_channel.send(f"Now playing {queue[0].split('/')[-1].split('.')[0]}")
        while not vc.is_playing():
            vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path,
                    source=queue[0]))
        while vc.is_playing():
            await asyncio.sleep(0.1)
        if not loop:
            os.remove(queue[0])
            queue.pop(0)
            update_queue()
        else:
            queue.append(queue.pop(0))
            update_queue()
    if not paused:
        await music_channel.send("Queue has ended")

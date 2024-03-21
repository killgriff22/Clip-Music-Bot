from classes import *
#
#
vc: discord.voice_client.VoiceClient | None = None
instances = []
def update_queue(queue=queue):
    open("queue.txt", "w").write(str(queue))

def read_queue():
    return eval(open("queue.txt").read())

@user.event
async def on_ready():
    global vc
    print(f'{user.user.name} has connected to Discord!')
    user_prompt_timeout.start()
    status.start()
    voice_channel = user.get_guild(1085995033037127750).get_channel(1088131367587565628)
    vc = await voice_channel.connect()
    queue_loop.start()
    instance_loop.start()


@user.event
async def on_message(message: discord.Message):
    global vc, queue, paused, loop
    if message.author == user.user: # dont respond to our own messages
        return
    if not message.content.startswith('!'): # check for the prefix
        return
    #this next chunk of code does some file fuckery and adds a status
    #one of the aliases for this command is !s. why? Dont ask me! i just work here!
    for _ in [""]: #allows me to skip this entire chunk of code if i try to stop the queue
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
    if not message.channel.id in [1215317925049667594, 1164386048407781457]: # this bot runs in a server with my friends and thats it, i dont want to clog chat so i whitlelist 2 channels
        return
    split = message.content.split(' ')
    match split[0]: #Downloading & Playlists & join command
        case '!download' | '!d':
            command = message.content.split(' ')
            if "https" in command[1]:  # Given a link
                msg = await message.channel.send(f"downloading {command[1]}")
                await msg.edit(suppress=True)
                instances.append(Instance(message, command[1]))
            elif command[1].isdigit():  # Given a number, assume we want to select from a list
                for user_ in users.copy():
                    if user_.user == message.author:
                        url = user_.search_urls[int(command[1])]
                        await message.channel.send(f"downloading {url}")
                        instances.append(Instance(message, url))
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
        case '!join' | '!j':
            if vc:
                await vc.disconnect()
            if len(split) == 2:
                match split[1]:
                    case '2':
                        vc = await message.guild.get_channel(1088131367587565628).connect()
                    case '1':
                        vc = await message.guild.get_channel(1170801016577458278).connect()
#                    case '3':
#                        vc = await message.guild.get_channel(1217156460769968250).connect()
                    case _:
                        vc = await message.author.voice.channel.connect()
            vc = await message.author.voice.channel.connect()
    if not vc:
        return
    match split[0]: #Music Bot Commands. Dependent on a active voice channel.
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
        case '!play' | '!p':
            paused = False
            if len(split) >= 2:
                url = split[1]
                command = split
                if "https" in url:
                    instances.append(Instance(message, url))
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
        case '!disconnect' | '!dc':
            await vc.disconnect()
            vc = None
@tasks.loop(seconds=1)
async def user_prompt_timeout(): #Controls user prompt timeouts...
    for user_ in users.copy():
        if user_.timeout > 0:
            user_.timeout -= 1
        else:
            users.remove(user_)
            await user.get_channel(1215317925049667594).send(f"{user_.user.name} timed out")


@tasks.loop(seconds=20)
async def status(): # manages the random status
    with open('statuses.txt', 'r') as f:
        statuses = f.readlines()
        for i, status in enumerate(statuses.copy()):
            statuses[i] = status.strip()
    await user.change_presence(activity=Custom_listening_activity(name=random.choice(statuses)))


@tasks.loop(seconds=1)
async def queue_loop(): #manages the queue
    if not vc: #dont run any of this if vc is None
        return
    if paused:# if the pause flag is set, pause the stream, the always return until unpaused
        if vc.is_playing():
            vc.pause()
        else:
            return
    global queue
    queue = read_queue()
    if not queue:# if the queue is empty, do nothing
        return
    music_channel = user.get_guild(
        1085995033037127750).get_channel(1164386048407781457)
    while queue:#while we have a queue, play the first item from the queue
        await music_channel.send(f"Now playing {queue[0].split('/')[-1].split('.')[0]}")
        while not vc.is_playing():#repeatedly try to play the song
            vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path,
                    source=queue[0]))
        while vc.is_playing():#wait until the song finishes
            await asyncio.sleep(0.1)
        if not loop:# if we arent looping, remove the file, and the entry, then update the queue file
            os.remove(queue[0])
            queue.pop(0)
            update_queue()
        else:# otherwise, send the firs item to the back and update the queue file
            queue.append(queue.pop(0))
            update_queue()
    await music_channel.send("Queue has ended") #when the queue is empty, say it!

@tasks.loop(seconds=4)
async def instance_loop():
    global instances
    for instance in instances.copy():
        instance:Instance = instance
        if instance.poll() != None:
            print("Instance finished")
            instances.remove(instance)
            msg = await instance.channel.send(f"Downloaded {instance.url}")
            await msg.edit(suppress=True)
    #os.walk through the downloads folder and send all mp3s to the music channel
            for root, dirs, files in os.walk("Downloads"):
                for file in files:
                    if "mp3" in file:
                        await user.get_guild(1085995033037127750).get_channel(1164386048407781457).send(files=[discord.File(os.path.join(root, file))])
                        os.remove(os.path.join(root, file))
from modules import *

class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class Spotify:
    def download_url(url):
        # os change working dir
        before_download = os.listdir(Spotify_path)
        print(f"downloading {url}")
        os.chdir(Spotify_path)
        os.system(f"spotdl {url}")
        os.chdir(os.path.join(os.getcwd(), root))
        after_download = os.listdir(Spotify_path)
        filename = list(set(after_download) - set(before_download))[0]
        return filename


class Youtube:
    def download_url(url):
        # os change working dir
        before_download = os.listdir(Youtube_path)
        os.chdir(Youtube_path)
        video = YouTube(url)
        video.streams.filter(only_audio=True).first().download()
        after_download = os.listdir(Youtube_path)
        filename = list(set(after_download) - set(before_download))[0]
        os.system(f'ffmpeg -i "{filename}" -vn -ab 128k -ar 44100 -y "{filename[:-4]}.mp3"')
        os.remove(filename)
        os.chdir(root)
        after_download = os.listdir(Youtube_path)
        filename = list(set(after_download) - set(before_download))[0]
        return filename


class Soundcloud:
    def download_url(url):
        # os change working dir
        before_download = os.listdir(Soundcloud_path)
        print(f"downloading {url}")
        os.chdir(Soundcloud_path)
        os.system(f"scdl -l {url}")
        os.chdir(root)
        after_download = os.listdir(Soundcloud_path)
        filename = list(set(after_download) - set(before_download))[0]
        return filename
    
class User:
    def __init__(self, user):
        self.user: discord.User = user
        self.search_urls = []
        self.timeout = 60

class Custom_listening_activity(discord.BaseActivity):
    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.kwargs = kwargs.copy()
        try:
            timestamps: discord.ActivityTimestamps = kwargs['timestamps']
        except KeyError:
            self._start = 0
            self._end = 0
        else:
            self._start = timestamps.get('start', 0)
            self._end = timestamps.get('end', 0)
    @property
    def type(self) -> discord.ActivityType:
        return discord.ActivityType.listening
    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Listening name={self.name!r}>'
    def to_dict(self) -> discord.Activity:
        timestamps: dict[str, any] = {}
        if self._start:
            timestamps['start'] = self._start

        if self._end:
            timestamps['end'] = self._end

        return {
            'type': discord.ActivityType.listening.value,
            'name': str(self.name),
            'timestamps': timestamps,  # type: ignore
            'assets':self.kwargs.get('assets', {}),
            'details':self.kwargs.get('details', ''),
        }
class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: discord.Message, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: discord.Message, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)

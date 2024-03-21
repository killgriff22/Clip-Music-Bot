from modules import *


class Spotify:
    def download_url(url):
        # os change working dir
        before_download = os.listdir(Spotify_path)
        print(f"downloading {url}")
        os.chdir(Spotify_path)
        os.system(f"./bin/spotdl {url}")
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
        os.system(f'{ffmpeg_path} -i "{filename}" -vn -ab 128k -ar 44100 -y "{filename[:-4]}.mp3"')
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
        os.system(f"./bin/scdl -l {url}")
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


class Instance(subprocess.Popen):
    def __init__(self,message, url, queue = False):
        print("New instance created")
        command = ["bin/python3","downloader.py",url]
        if queue:
            command.append("queue") 
        super().__init__(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,universal_newlines=True,shell=True)
        self.content = message.content
        self.author = message.author
        self.channel = message.channel
        self.guild = message.guild
        self.url = url
    def __str__(self):
        return self.content
    def __repr__(self):
        return f'<instance {self.content}>'
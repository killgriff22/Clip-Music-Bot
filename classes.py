from modules import *


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
        os.system(f"youtube-dl {url}")
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
        self.timeout = 3
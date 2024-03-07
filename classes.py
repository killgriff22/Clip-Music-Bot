from modules import *


class Spotify:
    def download_url(url):
        # os change working dir
        print(f"downloading {url}")
        os.chdir(Spotify_path)
        os.system(f"spotdl {url}")
        os.chdir(os.path.join(os.getcwd(), root))
        file_name = ""
        for artist in spotify.track(url)["artists"]:
            file_name += artist["name"] + ", "
        file_name = file_name[:-2]
        return f"{file_name} - {spotify.track(url)['name']}"


class Youtube:
    def download_url(url):
        # os change working dir
        os.chdir(Youtube_path)


class Soundcloud:
    def download_url(url):
        # os change working dir
        print(f"downloading {url}")
        os.chdir(Soundcloud_path)
        os.system(f"scdl -l {url}")
        os.chdir(os.path.join(os.getcwd(), root))
        artist, track = url.split("/")[-2], url.split("/")[-1]
        return f"{artist} - {track}"

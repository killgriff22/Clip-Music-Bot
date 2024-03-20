import sys
import os
from functions import *
args = sys.argv
queue = read_queue()
print(os.getcwd())
if "spotify" in args[1]:
    file = Spotify_path + Spotify.download_url(args[1])
elif "youtu" in args[1]:
    file = Youtube_path + Youtube.download_url(args[1])
elif "soundcloud" in args[1]:
    file = Soundcloud_path + Soundcloud.download_url(args[1])
print(os.getcwd)
queue.append(file)
update_queue()
import sys
import os
from functions import *
args = sys.argv
if len(args) < 2:
    print("No url provided")
    sys.exit()
elif len(args) > 2:
    queue = read_queue()
if "spotify" in args[1]:
    file = Spotify_path + Spotify.download_url(args[1])
elif "youtu" in args[1]:
    file = Youtube_path + Youtube.download_url(args[1])
elif "soundcloud" in args[1]:
    file = Soundcloud_path + Soundcloud.download_url(args[1])
if len(args) > 2:
    queue.append(file)
    update_queue(queue)
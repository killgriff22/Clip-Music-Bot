import sys
import os
from classes import *
args = sys.argv
queue = eval(open("queue.txt").read())
if "spotify" in args[1]:
    file = Spotify_path + Spotify.download_url(args[1])
elif "youtu" in args[1]:
    file = Youtube_path + Youtube.download_url(args[1])
elif "soundcloud" in args[1]:
    file = Soundcloud_path + Soundcloud.download_url(args[1])
queue.append(file)
open("queue.txt","w").write(str(queue))
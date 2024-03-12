try:
    import discord
    import requests
    import os
    from discord.ext import tasks
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from ytmusicapi import YTMusic
    from pytube import YouTube, Playlist
except ImportError:
    import os
    os.system(
        "pip install pytube spotdl scdl requests spotipy discord.py discord.py")
    import discord
    import requests
    from discord.ext import tasks
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from ytmusicapi import YTMusic
    from pytube import YouTube, Playlist
    import youtube_dl
from config import *
import random
import asyncio
import functools
import itertools
import math
from time import sleep
from atexit import register
import subprocess
users = []
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=spotipy_creds["client_id"],
        client_secret=spotipy_creds["client_secret"]
    )
)
user = discord.Client(intents=discord.Intents.all())
queue = eval(open("queue.txt").read())
Spotify_path = os.path.join(os.getcwd(), "Downloads/Spotify/")
Youtube_path = os.path.join(os.getcwd(), "Downloads/Youtube/")
Soundcloud_path = os.path.join(os.getcwd(), "Downloads/Soundcloud/")
root = os.getcwd()

def clean_exit():
    for file in os.listdir(Spotify_path):
        os.remove(Spotify_path+file) if "mp3" in file else None
    for file in os.listdir(Youtube_path):
        os.remove(Youtube_path+file) if "mp3" in file else None
    for file in os.listdir(Soundcloud_path):
        os.remove(Soundcloud_path+file) if "mp3" in file else None
from config import *
import discord
import requests
import os
from discord.ext import tasks
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
users = []
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=spotipy_creds["client_id"],
        client_secret=spotipy_creds["client_secret"]
        )
    )
user = discord.Client(intents=discord.Intents.all())
queue = []
Spotify_path = os.path.join(os.getcwd(), "Downloads/Spotify/")
Youtube_path = os.path.join(os.getcwd(), "Downloads/Youtube/")
Soundcloud_path = os.path.join(os.getcwd(), "Downloads/Soundcloud/")
root = os.getcwd()

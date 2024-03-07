from config import *
import discord
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=spotipy_creds["client_id"],
        client_secret=spotipy_creds["client_secret"]
    ))
user = discord.Client(intents=discord.Intents.all())

Spotify_path = os.path.join(os.getcwd(), "Downloads/Spotify/")
Youtube_path = os.path.join(os.getcwd(), "Downloads/Youtube/")
Soundcloud_path = os.path.join(os.getcwd(), "Downloads/Soundcloud/")
root = "/".join(Spotify_path.split("/")[:-3])+"/"

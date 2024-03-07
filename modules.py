from config import *
import discord
import requests
import os
from discord.ext import tasks
user = discord.Client(intents=discord.Intents.all())
queue = []
Spotify_path = os.path.join(os.getcwd(), "Downloads/Spotify/")
Youtube_path = os.path.join(os.getcwd(), "Downloads/Youtube/")
Soundcloud_path = os.path.join(os.getcwd(), "Downloads/Soundcloud/")
root = os.getcwd()

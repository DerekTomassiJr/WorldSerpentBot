import discord
import random

class siege_bot(discord.Client):
    def __init__(self, message, client):
        self.client = client
        self.channel = message.channel

        print("Siege Bot Initialized")
        print("Text Channel Detected: " + self.channel.name)

        self.bot_active = True
        

    # Initialization Variables
    client = None # World Serpent Bot Client
    channel = None # Message Text Channel
    bot_active = False # Flag for bots active status
    
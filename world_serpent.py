import discord
from discord.ext import commands
import random
from SiegeBotFiles import siege_bot
import cs_bot
import subprocess
from bot_token import TOKEN

# Constants
VERSION = "1.1.1"
DEBUG_ON = True
WORLD_SERPENT_NAME = "Jörmungandr#9126"
WILL_USER_ID = 752341726487904316

# Media
DONKEY_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1323437159503630436/6VDRd5.gif?ex=67748267&is=677330e7&hm=916a303d2deec35b9d8e106c2c6b4d429014dcd21cd02754379dc64714eac39f&"
SLIDE_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1327483349308280934/cop-cop-slide.gif?ex=67833ab5&is=6781e935&hm=3950f1175aa01bb84b2ce1fc0a1e7c9585f8384e68fd6aae107c8509d0cc173a&"
LUCA_PIC = "https://cdn.discordapp.com/attachments/375964855846305793/1381350838177366096/LucaBald.png?ex=684732b8&is=6845e138&hm=8f5446d9090301548ec06cdcbd1b4fefcb2f55a8f304e06cf0daf29152cb5435&"
LUCA_MOG_PIC = "https://cdn.discordapp.com/attachments/375964855846305793/1381354448797958164/LucaMog.png?ex=68473614&is=6845e494&hm=efde3b65c2b99fc85166c2284cc43dc8022dc49ce3b53bdb4ec7ed285c1141b9&"
WILL_GIF = "https://cdn.discordapp.com/attachments/790017647365980241/1410362828648480838/AutismLight.gif?ex=68b0be3d&is=68af6cbd&hm=71f7c092f4222a338d88bd461be6e7289c66c5b382468f2a21aadfc1427054eb&"

class world_serpent(commands.Bot):
# Track active bots per channel
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.active_bots = {}

    async def setup_hook(self):
    #Load Cogs 
        cogCategories = [
            "cogs.fun",
            "cogs.games",
            "cogs.blackjack",
            "cog.utilities"
        ]

        for ext in cogCategories:
            await self.load_extension(ext)
            print(ext + " Loaded")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        if DEBUG_ON:
            self.channel = "test"
            print(f'Debug Mode Enabled! Channel set to #{bot.channel}')

    async def on_message(self, message):
        # Debug Logging
        print("On_Message Triggered!")

        # Do not trigger if the author is this bot
        if str(message.author) == WORLD_SERPENT_NAME:
            print("Bot Message")
            return

        # Random Will GIF
        if (message.author.id == WILL_USER_ID and random.randint(1, 25) == 25):
                await message.channel.send(WILL_GIF)

        # Handle custom bots
        if message.channel.id in self.active_bots:
            bot_instance = self.active_bots[message.channel.id]
            if bot_instance.bot_active and message.content.startswith("!"):
                await bot_instance.command_handler(message.content)
            else:
                del self.active_bots[message.channel.id]

        await self.process_commands(message)  # Ensure commands still run

# create instance of Bot
bot = world_serpent()

# Start bot
bot.run(TOKEN)
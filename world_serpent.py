import discord
import cs_bot
import object_handler
from bot_token import TOKEN

class world_serpent(discord.Client):
    # Global variables
    channels = ["test", "general", "none_peasants"]
    counter_bot = None
    
    async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            print('------')

    async def on_message(self, message):
        #Debug Logging
        print("On_Message Triggered!")

        if (str(message.channel) in self.channels):
            cs_commands = ["!csprivatematch", "!csconfirmteams", "!csreroll", "!csendgame"]

            # Do not trigger if the author is this bot
            if (str(message.author) == WORLD_SERPENT_NAME):
                print("Bot Message")
                return

            # Commands
            if (message.content == "!test"):
                print("!test Command Triggered by: " + str(message.author))
                await message.channel.send("Hello!")

            if (message.content == "!move"):
                await message.channel.send(DONKEY_GIF)

            if (message.content == "!slidein"):
                await message.channel.send(SLIDE_GIF)
            
            is_cs_command = next((True for command in cs_commands if command in message.content), False)
            if (is_cs_command):
                print("!cs Command Triggered by: " + str(message.author))
                await message.channel.send("Valid CS Command") #debug
                
                if (self.counter_bot == None):
                    self.counter_bot = cs_bot.cs_bot(message)
                    await message.channel.send("CS Bot Actions Active!")
                
                cs_message = self.counter_bot.command_handler(message.content)
                print(cs_message)
                await message.channel.send(cs_message)

# CONSTANTS
WORLD_SERPENT_NAME = "Jörmungandr#9126"

# GIF CONSTANRTS
DONKEY_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1323437159503630436/6VDRd5.gif?ex=67748267&is=677330e7&hm=916a303d2deec35b9d8e106c2c6b4d429014dcd21cd02754379dc64714eac39f&"
SLIDE_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1327483349308280934/cop-cop-slide.gif?ex=67833ab5&is=6781e935&hm=3950f1175aa01bb84b2ce1fc0a1e7c9585f8384e68fd6aae107c8509d0cc173a&"

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)
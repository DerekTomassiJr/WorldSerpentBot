import discord
import cs_bot
from bot_token import TOKEN

class world_serpent(discord.Client):
    # Global variables
    channels = ["test", "general", "none_peasants"]
    active_bots = {}
    
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
            
            # create active bots
            if (message.content == "!startcsbot"):
                print("Creating cs bot! Triggerd by: " + str(message.author))
                self.active_bots[message.author.id] = cs_bot.cs_bot(message, client)
                await message.channel.send("CS Bot Actions Active!")
                return
            
            # temp fix for now
            if (message.content == "!stopallcsbots"):
                print("Stopping all active cs bot")
                self.active_bots = {}
                await message.channel.send("Deactivated all bots!!!")
                return

            # handle active bots
            if (message.author.id in self.active_bots):
                if (self.active_bots[message.author.id].bot_active):
                    await self.active_bots[message.author.id].command_handler(message.content)
                else:
                    del active_bots[message.author.id]

# CONSTANTS
WORLD_SERPENT_NAME = "Jörmungandr#9126"

# GIF CONSTANRTS
DONKEY_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1323437159503630436/6VDRd5.gif?ex=67748267&is=677330e7&hm=916a303d2deec35b9d8e106c2c6b4d429014dcd21cd02754379dc64714eac39f&"
SLIDE_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1327483349308280934/cop-cop-slide.gif?ex=67833ab5&is=6781e935&hm=3950f1175aa01bb84b2ce1fc0a1e7c9585f8384e68fd6aae107c8509d0cc173a&"

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)
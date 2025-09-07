import discord
import random
import Python.SnakeServerBot.CSBotFiles.cs_bot as cs_bot
from SiegeBotFiles import siege_bot
import Python.SnakeServerBot.CSBotFiles.cs_bot as cs_bot
from bot_token import TOKEN

class world_serpent(discord.Client):
    # Global variables
    channel = "snake-den"
    active_bots = {}
    general_commands = {}
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
        # Populating the general commands dictionary
        self.general_commands = {
            "!test" : "Hello!",
            "!version": f"Jörmungandr v{VERSION}",
            "!move": DONKEY_GIF,
            "!slidein": SLIDE_GIF,
            "!luca": LUCA_PIC,
            "!lucamog": LUCA_MOG_PIC
        }

        if DEBUG_ON:
            self.channel = "test"
            print(f'Debug Mode Enabled!!! Switching channel to {self.channel}');

    async def on_message(self, message):
        #Debug Logging
        print("On_Message Triggered!")

        if (str(message.channel) == self.channel):
            # Do not trigger if the author is this bot
            if (str(message.author) == WORLD_SERPENT_NAME):
                print("Bot Message")
                return

            # Commands
            if (message.content in self.general_commands.keys()):
                await message.channel.send(self.general_commands[message.content])

            if (message.author.id == WILL_USER_ID and random.randint(1, 25) == 25):
                await message.channel.send(WILL_GIF)
          
            # Create active bots
            if (message.content == "!startcsbot"):
                print("Creating cs bot! Triggerd by: " + str(message.author))
                self.active_bots[message.channel.id] = cs_bot.cs_bot(message, client)
                if (self.active_bots[message.channel.id].bot_active):
                    await message.channel.send("CS Bot Actions Active!")
                else:
                    await message.channel.send("CS Bot did not initialize properly!")
                return
            
            if (message.content == "!startsiegebot"):
                print("Creating Siege Bot! Triggered by: " + str(message.author))
                self.active_bots[message.channel.id] = siege_bot.siege_bot(message, client)
                await message.channel.send("Siege Bot Activated")
                return

            # Handle active bots
            if (message.channel.id in self.active_bots and message.content.startswith("!")):
                if (self.active_bots[message.channel.id].bot_active):
                    await self.active_bots[message.channel.id].command_handler(message.content)
                else:
                    del self.active_bots[message.channel.id]
                    
            # Kill switch for a last resort
            if (message.content == "!stopallsubbots" and message.author.guild_permissions.administrator):
                print("Stopping all active sub bots")
                self.active_bots = {}
                await message.channel.send("Deactivated all sub bots!!!")
                return
            
            await self.debug_commands(message)
            
    async def debug_commands(self, message):
        if (message.content == "!displayactivesubbots"):
            await message.channel.send(f"Active Sub Bots:\n{self.active_bots}")

# CONSTANTS
WORLD_SERPENT_NAME = "Jörmungandr#9126"
VERSION = "1.1.2"
WILL_USER_ID = 752341726487904316
DEBUG_ON = True

# GIF CONSTANRTS
DONKEY_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1323437159503630436/6VDRd5.gif?ex=67748267&is=677330e7&hm=916a303d2deec35b9d8e106c2c6b4d429014dcd21cd02754379dc64714eac39f&"
SLIDE_GIF = "https://cdn.discordapp.com/attachments/1136020852090093579/1327483349308280934/cop-cop-slide.gif?ex=67833ab5&is=6781e935&hm=3950f1175aa01bb84b2ce1fc0a1e7c9585f8384e68fd6aae107c8509d0cc173a&"
LUCA_PIC = "https://cdn.discordapp.com/attachments/375964855846305793/1381350838177366096/LucaBald.png?ex=684732b8&is=6845e138&hm=8f5446d9090301548ec06cdcbd1b4fefcb2f55a8f304e06cf0daf29152cb5435&"
LUCA_MOG_PIC = "https://cdn.discordapp.com/attachments/375964855846305793/1381354448797958164/LucaMog.png?ex=68473614&is=6845e494&hm=efde3b65c2b99fc85166c2284cc43dc8022dc49ce3b53bdb4ec7ed285c1141b9&"
WILL_GIF = "https://cdn.discordapp.com/attachments/790017647365980241/1410362828648480838/AutismLight.gif?ex=68b0be3d&is=68af6cbd&hm=71f7c092f4222a338d88bd461be6e7289c66c5b382468f2a21aadfc1427054eb&"

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)

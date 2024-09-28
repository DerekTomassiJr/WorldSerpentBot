import discord
import cs_bot
import object_handler
from bot_token import TOKEN

class world_serpent(discord.Client):
    # Global variables
    channels = ["test"]#, "general"]
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

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)
import discord
import cs_bot
from bot_token import TOKEN

# Global variables
channels = ["test", "general"]
cs_bot = None

class world_serpent(discord.Client):
    async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            print('------')

    async def on_message(self, message):
        #Debug Logging
        print("On_Message Triggered!")

        if (str(message.channel) in channels):
            cs_commands = ["!csprivatematch", "!csconfirmteams"]

            # Commands
            if (message.content == "!test"):
                print("!test Command Triggered by: " + str(message.author))
                await message.channel.send("Hello!")
            
            is_cs_command = next((True for command in cs_commands if command in message.content), False)
            if (is_cs_command):
                print("!cs Command Triggered by: " + str(message.author))
                await message.channel.send("Valid CS Command") #debug
                
                # if (cs_bot == None):
                #     cs_bot = cs_bot(message)
                #     await message.channel.send("CS Bot Actions Active!")
                
                # cs_bot.command_handler(message.content)

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)
import discord
from bot_token import TOKEN

# Global variables
channels = ["test"]

class world_serpent(discord.Client):
    async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            print('------')

    async def on_message(self, message):
        #Debug Logging
        print("On_Message Triggered!")

        if (str(message.channel) in channels):

            # Commands
            if (message.content == "!test"):
                print("!test Command Triggered by: " + str(message.author))
                await message.channel.send("Hello!")

client = world_serpent(intents=discord.Intents.all())
client.run(TOKEN)
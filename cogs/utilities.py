from discord.ext import commands
import discord
import git
import os
import sys

VERSION = "1.2.0"

class Utilities(commands.Cog):
    """Cog for bot-related commands like Version, Pictures and GIFs."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'version', 
                      help = 'Displays the current version of the bot', 
                      brief = 'Bot Version',
                      usage = '!version')
    async def version(self, ctx):
        print("!version Command Triggered by: " + str(ctx.author))
        await ctx.send(f"Jörmungandr v{VERSION}")
        
    @commands.command(name='update',
                      help="Updates the bot to the latest released version.",
                      brief = 'Bot Update',
                      usage="!update")
    async def update(self, ctx):
        print("!update Command Triggered by: " + str(ctx.author))
        if ctx.author.guild_permissions.administrator:
            print(f"Update triggered by: {ctx.author}")
            await ctx.send("An update has been triggered. Please wait while update is in progress...")
            
            g = git.cmd.Git("C:/users/derek/Documents/Code/Python/SnakeServerBot")
            g.pull()
            
            print("Jormungander restarting...")
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await ctx.author.send("You do not have permission to access this command! This is made only for user with administrator permissions.")
            print(f'{ctx.author} tried to access the update command without valid permissions! The user has been notified.')


async def setup(bot):
    print("Loading Utilties Cog...")
    await bot.add_cog(Utilities(bot))
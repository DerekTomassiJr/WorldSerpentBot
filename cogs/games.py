from discord.ext import commands
import cs_bot
from SiegeBotFiles import siege_bot

class GamesBot(commands.Cog):
    """Cog for game-related commands like CS Bot and Siege Bot."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'startcsbot', help = 'Starts the CS Bot in the current channel', brief = 'Start CS Bot')
    async def startcsbot(self, ctx):
        print("Creating CS bot! Triggered by: {ctx.author}" )
        self.bot.active_bots[ctx.channel.id] = cs_bot.cs_bot(ctx.message, self.bot)
        await ctx.send("CS Bot Activated!")

    @commands.command(name = 'startsiegebot', help = 'Starts the Siege Bot in the current channel', brief = 'Start Siege Bot')
    async def startsiegebot(self, ctx):
        print("Creating Siege bot! Triggered by: {ctx.author}" )
        self.bot.active_bots[ctx.channel.id] = siege_bot.siege_bot(ctx.message, self.bot)
        await ctx.send("Siege Bot Activated!")

    @commands.command(name = 'stopallcsbots', help = 'Stops all active CS Bots', brief = 'Stop all CS Bots')
    async def stopallcsbots(self, ctx):  
        self.bot.active_bots.clear()
        await ctx.send("All CS bots deactivated.")

async def setup(bot):
    print("Loading Games Cog...")
    await bot.add_cog(GamesBot(bot))
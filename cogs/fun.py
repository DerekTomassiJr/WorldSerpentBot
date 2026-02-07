from discord.ext import commands
import discord
import yt_dlp

VERSION = "1.1.1"

class SnakeBot(commands.Cog):
    """Cog for bot-related commands like Version, Pictures and GIFs."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'donkey', help = 'Sends Donkey GIF', brief = 'Donkey GIF')
    async def donkey(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/1136020852090093579/1323437159503630436/6VDRd5.gif?ex=67748267&is=677330e7&hm=916a303d2deec35b9d8e106c2c6b4d429014dcd21cd02754379dc64714eac39f&")

    @commands.command(name ='slidein', help = 'Cop Slide GIF', brief = 'Slide GIF')
    async def slidein(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/1136020852090093579/1327483349308280934/cop-cop-slide.gif?ex=67833ab5&is=6781e935&hm=3950f1175aa01bb84b2ce1fc0a1e7c9585f8384e68fd6aae107c8509d0cc173a&")

    @commands.command(name = 'luca', help = 'Sends Luca Picture', brief = 'Luca Picture')
    async def luca(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/375964855846305793/1381350838177366096/LucaBald.png?ex=684732b8&is=6845e138&hm=8f5446d9090301548ec06cdcbd1b4fefcb2f55a8f304e06cf0daf29152cb5435&")

    @commands.command(name = 'lucamog', help = 'Sends Luca Mog Picture', brief = 'Luca Mog Picture')
    async def lucamog(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/375964855846305793/1381354448797958164/LucaMog.png?ex=68473614&is=6845e494&hm=efde3b65c2b99fc85166c2284cc43dc8022dc49ce3b53bdb4ec7ed285c1141b9&")

async def setup(bot):
    print("Loading Fun Cog...")
    await bot.add_cog(SnakeBot(bot))
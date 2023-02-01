import nextcord
from nextcord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["h"])
    async def helpme(self, ctx):
        embed = nextcord.Embed(title="Commands for Jabs Bot")
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/1003251203158843454/1003325054022602855/sdad.jpg")
        embed.add_field(
            name="Basic Commands",
            value="`j!hello` - Obi Wan Gif Meme\n",
            inline=False)
        embed.add_field(
        name="Server Commands",
            value="`j!clear [value]` - Deletes messages\n",
            inline=False)
        embed.add_field(
            name="Gif/Meme Commands",
            value="`j!gif [name]` - searches and displays your gif\n`j!meme` - Gif Meme\n",
            inline=False)
        embed.add_field(
            name="Music Commands",
            value=
            "`j!play[song_name or url]` or `j!p[name or url]` - Plays a music from YouTube and Spotify.\n`j!resume` - Resumes the music.\n`j!skip` - Skips a music.\n`j!shuffle` - Shuffles your queue.\n`j!queue` or `j!q` - Display current queue musics.\n`j!loop` - Loops the music.\n`j!leave` - Leaves the channel.\n`j!lyric [name]` - searches and displays the lyric.\n",
            inline=False)
        
        return await ctx.send(embed=embed)

    @commands.command(aliases=["hi"])
    async def hello(self, ctx):
        await ctx.send('https://c.tenor.com/6us3et_6HDoAAAAC/hello-there-hi-there.gif')
    @commands.command()
    async def beng(self,ctx):
        await ctx.send('https://media.discordapp.net/attachments/1001197595990966306/1002811220325310484/727790300923166771.gif')
    @commands.command()
    async def seph(self,ctx):
        await ctx.send('https://c.tenor.com/_73fKmyXkVYAAAAC/fbi-fbiopenup.gif')

def setup(bot):
    bot.add_cog(Basic(bot))
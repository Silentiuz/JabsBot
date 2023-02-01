import os
from lyricsgenius import Genius
from nextcord.ext import commands, menus

from .paginator.lyricprovider import LyricBody

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=['lyrics'])
    async def lyric(self, ctx: commands.Context, *, search: str):
        genius =Genius(os.environ['Genius'])
        song = genius.search_song(search)
        data = song.lyrics
        pages = menus.ButtonMenuPages(
            source=LyricBody(data),
            disable_buttons_after=True)
        await pages.start(ctx)

def setup(bot):
    bot.add_cog(Lyrics(bot))
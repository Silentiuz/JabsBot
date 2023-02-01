import nextcord
from nextcord.ext import menus

class LyricBody(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1999)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Lyrics", description=entries)
        embed.set_footer(text=f'Powered by: Genius')
        return embed

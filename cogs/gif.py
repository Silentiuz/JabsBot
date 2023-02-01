import nextcord, random
from nextcord.ext import commands
import giphy_client
from giphy_client.rest import ApiException

class Gif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def gif(self, ctx, * ,q: str):
        
        api_key = 'sVC7MN17546akMi6KrD0wvkUw0vrSRcL'
        api_instance = giphy_client.DefaultApi()

        try:
            api_responce = api_instance.gifs_search_get(api_key, q, limit = 10)
            lst = list(api_responce.data)
            giff = random.choice(lst)

            await ctx.channel.send(giff.embed_url)

        except ApiException as e:
            print("Exception when calling Api")

    @commands.command()
    async def meme(self, ctx, * ,q = "latest meme"):
        
        api_key = 'sVC7MN17546akMi6KrD0wvkUw0vrSRcL'
        api_instance = giphy_client.DefaultApi()

        try:
            api_responce = api_instance.gifs_search_get(api_key, q, limit = 10)
            lst = list(api_responce.data)
            giff = random.choice(lst)

            await ctx.channel.send(giff.embed_url)

        except ApiException as e:
            print("Exception when calling Api")
    
def setup(bot):
    bot.add_cog(Gif(bot))
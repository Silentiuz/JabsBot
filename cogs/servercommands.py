from nextcord.ext import commands

class ServComm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        amount = amount + 1
  
        if amount > 101:
            await ctx.send("Cannot delete more than 100 messages!")
        else:
            await ctx.channel.purge(limit = amount)
            await ctx.send("Cleared Messages!", delete_after=3)
    
def setup(bot):
    bot.add_cog(ServComm(bot))

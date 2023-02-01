import nextcord, os
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.AutoShardedBot(shard_count=20,
                              command_prefix='j!',
                              intents=intents)


@bot.event
async def on_ready():
    print('Im alive madafaka!')
    await bot.change_presence(activity=nextcord.Activity(
        type=nextcord.ActivityType.listening, name='j!helpme | j!h'))


cogs = [
    "cogs.basic", "cogs.gif", "cogs.music", "cogs.lyrics",
    "cogs.servercommands"
]

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(cog + " was loaded.")
    except Exception as e:
        print(e)


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx):
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print("Cogs loaded!")
        except Exception as e:
            print(e)


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx):
    for cog in cogs:
        try:
            bot.unload_extension(cog)
            print("Cogs unloaded!")
        except Exception as e:
            print(e)


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    for cog in cogs:
        try:
            bot.reload_extension(cog)
            print("Cogs reloaded!")
        except Exception as e:
            print(e)


@bot.command()
@commands.has_permissions(administrator=True)
async def servernum(ctx):
    print(f"{len(bot.guilds)}")


bot.run(os.environ['DISCORD_TOKEN'])

import nextcord, wavelink, datetime, os, random, asyncio
from nextcord.ext import commands, menus
from wavelink.ext import spotify

from .paginator.queuepage import Queue


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    #connecting to server music
    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='krn.2d.gay',
            port=443,
            password='AWP)JQ$Gv9}dm.u',
            https=True,
            spotify_client=spotify.SpotifyClient(
                client_id="36f6b1219d0546608b9c4466a58b4a56",
                client_secret="7fac43a7fa3d42209161f58510f0536f"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player,
                                    track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        if vc.queue.is_empty:
            return await vc.stop()
                                      
        next_song = vc.queue.get()
        try:
            await vc.play(next_song)
            em = nextcord.Embed(title="Now playing! ",
                                description=f"{next_song.title}",
                                colour=15418782)
            await ctx.send(embed=em)
        except:
            pass


    @commands.command(aliases=["p"])  #PLAY YOUTUBE
    async def play(self, ctx: commands.Context, *, search: str):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Join a voice channel first! (╯°□°）╯︵ ┻━┻",
                                delete_after=30)
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        tracks=[]

        if vc.queue.is_empty and not vc.is_playing():
          
            try:
              if search.startswith("https://open.spotify.com/track/"):
                  try:
                    track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                    await vc.play(track)
                    em = nextcord.Embed(title="Now playing!", description=f"{track.title}", colour=15418782)
                    await ctx.send(embed=em)
                  except Exception as e:
                      emb = nextcord.Embed(title="Pleast enter a spotify song *url*", colour= 15548997)
                      await ctx.send(embed=emb)
                      return print(e)
                    
              elif search.startswith("https://open.spotify.com/playlist/"):
                  try:
                      async for track in spotify.SpotifyTrack.iterator(query=search, partial_tracks=True):
                        vc.queue.put(track)
                        tracks.append(track)
                      music = vc.queue.get()
                      embe = nextcord.Embed(title=f"Added {len(tracks)} tracks to the queue!", colour= 15418782)
                      await ctx.send(embed=embe)
                      em = nextcord.Embed(title="Now playing! ", description=f"{music.title}", colour= 15418782)
                      await ctx.send(embed=em)
                      await vc.play(music)
                  except Exception as e:
                      emb = nextcord.Embed(title="Pleast enter a spotify song *url*", colour= 15548997)
                      await ctx.send(embed=emb)
                      return print(e)
              
              else:
                  track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
                  await vc.play(track)
                  em = nextcord.Embed(title="Now playing! ", description=f"{track.title}", colour= 15418782)
                  await ctx.send(embed=em)
            except Exception as e:
                emb = nextcord.Embed(title="Invalid Input", colour= 15548997)
                await ctx.send(embed=emb)
                return print(e)
        else:
          
            try:
              if search.startswith("https://open.spotify.com/track/"):
                  try:
                    track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                    await vc.queue.put_wait(track)
                    em = nextcord.Embed(title="Queued: ",description=f"{track.title}", colour= 5793266)
                    await ctx.send(embed=em)
                  except Exception as e:
                      emb = nextcord.Embed(title="Pleast enter a spotify song *url*", colour= 15548997)
                      await ctx.send(embed=emb)
                      return print(e)
              elif search.startswith("https://open.spotify.com/playlist/"):
                  try:
                      async for track in spotify.SpotifyTrack.iterator(query=search, partial_tracks=True):
                        vc.queue.put(track)
                        tracks.append(track)
                      embe = nextcord.Embed(title=f"Added {len(tracks)} tracks to the queue!", colour= 15418782)
                      await ctx.send(embed=embe)
                  except Exception as e:
                      emb = nextcord.Embed(title="Pleast enter a spotify song *url*", colour= 15548997)
                      await ctx.send(embed=emb)
                      return print(e)
              else:
                  track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
                  await vc.queue.put_wait(track)
                  em = nextcord.Embed(title="Queued: ",description=f"{track.title}", colour= 5793266)
                  await ctx.send(embed=em)
                
            except Exception as e:
              emb = nextcord.Embed(title="Invalid Input", colour= 15548997)
              await ctx.send(embed=emb)
              return print(e)
      
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @commands.command()  #PAUSE
    async def pause(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.pause()
        emb = nextcord.Embed(title="Paused!", colour=15548997)
        await ctx.send(embed=emb)

    @commands.command()  #RESUME
    async def resume(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.resume()
        emb = nextcord.Embed(title="Resumed!", colour=5763719)
        await ctx.send(embed=emb)

    @commands.command()  #SKIP
    async def skip(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        emb = nextcord.Embed(title="Skipped!", colour=5763719)
        await ctx.send(embed=emb)

    @commands.command(aliases=['dc'])  #LEAVE
    async def leave(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        vc.queue.clear()
        await vc.stop()
        await vc.disconnect()
        emb = nextcord.Embed(title="Disconnected! *sino ba naman ako*!",
                             colour=7419530)
        await ctx.send(embed=emb)

    @commands.command()  #STOP
    async def stop(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            await vc.stop()
            vc.queue.clear()
            emb = nextcord.Embed(title="Stopped!", colour=15548997)
            await ctx.send(embed=emb)

        except Exception as e:
            return print(e)

    @commands.command()  #SHUFFLE
    async def shuffle(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            random.shuffle(vc.queue._queue)
        except Exception as e:
            return print(e)

        emb = nextcord.Embed(title="Shuffled!", colour=15105570)
        await ctx.send(embed=emb)

    @commands.command()  #LOOP
    async def loop(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            emb = nextcord.Embed(title="Loop is on!", colour=5763719)
            return await ctx.send(embed=emb)
        else:
            emb = nextcord.Embed(title="Loop is off!", colour=15548997)
            return await ctx.send(embed=emb)

    @commands.command(aliases=["q"])  #QUEUE
    async def queue(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            emb = nextcord.Embed(title="Queue is empty!", colour=5763719)
            return await ctx.send(embed=emb)

        fields = []
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            field = (u"\n\u200b", f"**{song_count})**{song.title}")
            fields.append(field)
        pages = menus.ButtonMenuPages(
            source=Queue(fields),
            clear_buttons_after=True,
        )
        await pages.start(ctx)

    @commands.command(aliases=['cp'])  #Display Current Music
    async def currplay(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send(
                "Join a voice channel first and play a music! -_-",
                delete_after=30)
        elif not ctx.voice_client:
            return await ctx.send("No Music playing!", delete_after=30)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            return await ctx.send("Nothing is playing!")

        em = nextcord.Embed(title=f"Now playing {vc.track.title}",
                            description=f"Artist: {vc.track.author}",
                            color=3426654)
        em.set_thumbnail(url=f"{vc.track.thumbnail}")
        em.add_field(
            name="Duration",
            value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Extra Info",
                     value=f"Song URL:[Click Me!]({str(vc.track.uri)})")
        return await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Music(bot))

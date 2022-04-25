import discord
import youtube_dl
from discord.ext import commands
from urllib3.util import url


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Ah ! Sorry, but you are not in any **voice channel**. I can't play music here, I don't want"
                           " to annoy anyone...")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(invoke_without_subcommand=True)
    async def play(self, ctx):
        ctx.voice_client.play(url)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused :pause_button:")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume
        await ctx.send("Resume :play_pause:")


def setup(bot):
    bot.add_cog(Music(bot))

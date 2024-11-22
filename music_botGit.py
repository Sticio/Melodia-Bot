import discord
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio
import os
import yt_dlp as yt_dlp_module

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Ensure the necessary directories exist
if not os.path.isdir("downloads"):
    os.makedirs("downloads")

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # Bind to IPv4 since IPv6 addresses cause issues sometimes
    'extract_flat': True,  # Extract only single entries, skip playlists
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -y',
    'options': '-vn -threads 1',
    'executable': r'C:\ffmpeg\ffmpeg-2024-06-21-git-d45e20c37b-essentials_build\bin\ffmpeg.exe'
}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp_module.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=not stream)
            if 'entries' in info:
                info = info['entries'][0]
            filename = info['url'] if stream else ydl.prepare_filename(info)
            return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=info)

# Music queue and state management
queue = []
loop = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, *, query):
    async with ctx.typing():
        query = f'ytsearch:{query}'
        player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
        queue.append(player)
        await ctx.send(f'**{player.title}** has been added to the queue.')

    if not ctx.voice_client.is_playing():
        await play_next(ctx)

async def play_next(ctx):
    if queue:
        player = queue.pop(0)
        ctx.voice_client.play(player, after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f'Now playing: **{player.title}**')
    elif loop:
        player = queue[-1]
        ctx.voice_client.play(player, after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f'Now playing (looping): **{player.title}**')

@bot.command(name='skip', help='Skips the currently playing song')
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

@bot.command(name='queue', help='Displays the current queue')
async def show_queue(ctx):
    if queue:
        msg = '\n'.join([f'**{i+1}. {player.title}**' for i, player in enumerate(queue)])
        await ctx.send(f'Current queue:\n{msg}')
    else:
        await ctx.send('The queue is empty.')

@bot.command(name='clear', help='Clears the queue')
async def clear(ctx):
    global queue
    queue = []
    await ctx.send('The queue has been cleared.')

@bot.command(name='loop', help='Loops the current song')
async def loop_(ctx):
    global loop
    loop = not loop
    await ctx.send(f'Looping is now {"enabled" if loop else "disabled"}.')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to a voice channel.')
        return

    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Tells the bot to leave the voice channel')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

bot.run('token')

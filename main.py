# bot.py
import os
import random

import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord.utils import get
from discord.voice_client import VoiceClient
from discord import utils, Client
from discord.ext.commands import Bot
import youtube_dl
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# bot = commands.Bot(command_prefix='oy cinike ')
# bot = commands.Bot(command_prefix='/')
# bot.remove_command('help')
# client = discord.Client() 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=']', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # await bot.change_presence(status=discord.Status.online, activity=discord.Game("ABC"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="H"))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Hyokina noise"))

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hoy {member.name} Goblog'
    )
    print(f'{member} telah join')

@bot.event
async def on_member_remove(member):
    print(f'{member} telah keluar')


@bot.command()
async def cekping(ctx):
    await ctx.send(f'{round(bot.latency * 100)}ms')

@bot.command(aliases=['Apakah', 'apakah'])
async def _69TnyaGoblok(ctx,*,pertanyaanKA):
    jawabanKA = ['Ya',
                 'Kurasa tidak',
                 'Tidak']
    await ctx.send(f'Pertanyaan: Apakah {pertanyaanKA}\nCinike: {random.choice(jawabanKA)}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Cinike tidak mengerti')

@bot.command()
async def bersihkan(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)

@bersihkan.error
async def c_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('error, masukan jumlah yang ingin dibersihkan')

@bot.command()
async def doctor(ctx):
    await ctx.send('( ͡° ͜ʖ ͡°)')

@bot.command()
async def s(ctx,*,msg):
    await ctx.message.delete()
    await ctx.send("{}".format(msg))
    
@bot.event
async def on_message(message):

    filter = ["ajg", "bgsd"]

    dictonari = {
        "hina adji" : 'adji gblg <@313318171215921154>',
        "hina pajrun" : "pajrun gblg <@256780323533094919>"
    }

    if message.author == bot.user:
        return

    if message.content in dictonari:
        await message.channel.send(dictonari[message.content])

    for word in filter:
        if message.content.count(word) > 0:
            print('%s berkata kasar' % (message.author.id))
            await message.channel.send('<@%s> berkata kasar' % (message.author.id))
    
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Cinike telah join ke {channel}\n")
    await ctx.send(f"Cinike join ke {channel}")

@bot.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Cinike telah join ke {channel}\n")
        await ctx.send(f"Cinike meninggalkan {channel}")
    else:
        await ctx.send(f"Hm ?")

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("error, cooldown")
        return

    # await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

bot.run(token)
# client.run(token)
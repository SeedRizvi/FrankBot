import os

import asyncio
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.voice_client import VoiceClient
from dotenv import load_dotenv
from random import randint

VOICE_CHANNEL = 'ball-channel'
WORK_CHANNEL = 'bot-tests'
ASAD = 'Daruni#8443'
cat_gif = 'https://tenor.com/view/good-night-flynn-flynn-park-flynn-gif-24987363'

load_dotenv()
TOKEN = os.getenv('DISCORDTOKEN')
GUILD = os.getenv('DISCORDSERVER')
# print(SERVER)

client = discord.Client()

data = {"guilds": []}
'''
data = {
    "guilds": [{"g_name": f, "channel": channel}]
}
'''

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("Launching Bot")
    await asyncio.sleep(7)
    '''
    print(bot.voice_clients)
    for vc in bot.voice_clients:
        print(f'Channel is {vc.channel}')
        print(len(vc.channel.members))
        if len(vc.channel.members) < 1:
            print('Disconnecting Bot')
            return await vc.disconnect()
    '''


@client.event
async def on_message(message):
    if message.author == bot.user:
        return
    '''
    print(f'{message.author} posted in {message.channel}')
    if str(message.author) != ASAD:
        print("not asad")
        return
    '''
    if str(message.channel) != WORK_CHANNEL:
        print("not in tests, ignoring")
        return

    print(f"New message from: {message.author}")
    # If the message was posted in the bot-tests channel
    if str(message.channel) == WORK_CHANNEL:
        await message.channel.send(message.content)
    if 'flynn' in str(message.content).lower():
        await message.channel.send(cat_gif)


@bot.command()
async def play(ctx, *args):
    to_play = ' '.join(args[0:])
    channel = ctx.author.voice.channel
    await channel.connect()

    '''
    author = ctx.message.author
    for member in discord.VoiceChannel:
        if member == author:
            print(member) 

    channel = author.voice_channel
    # await channel.connect()
    await VoiceChannel.connect(channel)
    
    if to_play == 'word':
        source = FFmpegPCMAudio(
            "https://www.youtube.com/watch?v=_YzD9KW82sk", executable="ffmpeg")
        ctx.voice_client.play(source, after=None)
    '''
    await ctx.send(f'Cannot play "{to_play}"')


@bot.command()
async def flynn(ctx):
    await ctx.send(cat_gif)


@bot.command()
async def flip(ctx):
    outcome = randint(1, 2)
    await ctx.send("Heads") if outcome == 1 else await ctx.send("Tails")


@bot.command()
async def meow(ctx):
    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="meow.mp3"))
    except:
        ctx.voice_client.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="meow.mp3"))


@bot.command()
async def boom(ctx):
    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="boom.mp3"))
    except:
        ctx.voice_client.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="boom.mp3"))


@bot.command()
async def bruh(ctx):
    filename = 'images/bruh.png'
    with open(filename, "rb") as fh:
        to_send = discord.File(fh, filename=filename)
        await ctx.send(file=to_send)


@bot.command()
async def disconnect(ctx):
    for vc in bot.voice_clients:
        if vc.guild == ctx.message.guild:
            return await vc.disconnect()
    return await ctx.send("Bot is not in any voice chat currently.")


@bot.command()
async def clear(ctx):
    global data
    data = {"guilds": []}
    return


@bot.event
async def timeout():
    print("Checking timeout")
    for vc in bot.voice_clients:
        if vc.channel.members < 1:
            return await vc.disconnect()
    pass


bot.run(TOKEN)

'''
@client.event
async def on_ready():
    # From the servers connected to Frank's Music, find YBS
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has found Server: {GUILD}(id: {guild.id})')
    channel = discord.utils.get(guild.channels, name=WORK_CHANNEL)
    print(f'The working channel is: {channel.name}')
    global data
    data['guilds'].append(dict(g_name=guild.name, channel=channel.name))
'''

import os

import asyncio
import discord
import youtube_dl
import validators
import json
import socket
import datetime
# import pycord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.voice_client import VoiceClient
from dotenv import load_dotenv
from random import randint
from items import get_items

# GLOBAL VARIABLES--------------------------------------------------------------
VOICE_CHANNEL = 'ball-channel'
WORK_CHANNEL = 'bot-tests'
ASAD = 'Daruni#8443'
cat_gif = 'https://tenor.com/view/good-night-flynn-flynn-park-flynn-gif-24987363'
RANDOM_GIF = 'https://tenor.com/view/crying-sobbing-uncontrollably-sad-cry-gif-19906768'
data = {"guilds": []}
song_queue = []
tasker = None
tasker_dig = None
now_playing = ""
data_file = "data.txt"
confirm = 0
confirm2 = 0
# ENVIRONMENT VARIABLES---------------------------------------------------------
load_dotenv()
TOKEN = os.getenv('DISCORDTOKEN')
GUILD = os.getenv('DISCORDSERVER')


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
ytdl_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': ip_address  # Change if IPv4 changes
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)


ffmpeg_options = {
    'options': '-vn'
}

bot = commands.Bot(command_prefix='!')


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.9):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.duration = data.get('duration')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{url}", download=not stream or play))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@bot.event
async def on_ready():
    print("Launching Bot")


@bot.command(name='play', aliases=['p', 'play_song'])
async def play(ctx, url: str, *args):
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    print(url)
    if not validators.url(url):
        # url = ' '.join(args[0:])
        to_play = url + " " + ' '.join(args[0:])
        print(to_play)
        url = to_play
    try:
        # If author is in vc join that channel, otherwise error
        if(voice == None):
            if not ctx.message.author.voice:
                await ctx.send(f"{ctx.author} is not connected to a voice channel")
            else:
                await ctx.author.voice.channel.connect()

        elif voice.channel != ctx.author.voice.channel:
            await ctx.send('I am already in another channel!')

        async with ctx.typing():
            # The bot's connection to a channel
            voice_client = ctx.message.guild.voice_client
            if not voice_client.is_playing() and not voice_client.is_paused():
                song_queue.clear()
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            if len(song_queue) == 0:
                await start_playing(ctx, player)

            else:
                song_queue.append(player)
                await ctx.send(f"**Queued at position {len(song_queue)-1}:** {player.title}")
    except Exception as error:
        print(f'An error has occured: {error}')


async def start_playing(ctx, player):
    global song_queue
    global now_playing
    song_queue.append(player)
    if (song_queue[0] == None):
        return
    i = 0
    while i < len(song_queue):
        try:
            # ctx.voice_client.play(song_queue[0], after=lambda e: print(
            #     'Player error: %s' % e) if e else None)
            ctx.voice_client.play(song_queue[0], after=lambda e: print(
                f'Player error: {e}') if e else None)
            now_playing = song_queue[0].title
            await ctx.send(f"**Now playing:** {song_queue[0].title}")
        except Exception as e:
            await ctx.send(f"Something went wrong: {e}")
        # await asyncio.sleep(song_queue[0].duration)
        global tasker
        tasker = asyncio.create_task(coro(ctx, song_queue[0].duration))
        try:
            await tasker
            now_playing = ""
        except asyncio.CancelledError:
            print("Task cancelled")
            now_playing = ""
        if(len(song_queue) > 0):
            song_queue.pop(0)


async def coro(ctx, duration):
    # Reconsider context, not really needed?
    await asyncio.sleep(duration)


@bot.command(name='queue', aliases=['q', 'list'])
async def queued(ctx):
    global song_queue
    a = ""
    i = 0
    for f in song_queue:
        if i > 0:
            a = a + str(i) + ". " + f.title + "\n "
        i += 1
    await ctx.send("Queued songs: \n " + a)


@bot.command(name='pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await ctx.send("Paused playing.")
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await ctx.send("Resumed playing.")
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='skip')
async def skip(ctx):
    global tasker
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        tasker.cancel()
        await ctx.send("Skipped song.")
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='nowplaying', aliases=['np', 'songs'])
async def queued(ctx):
    global now_playing
    await ctx.send(f'**CURRENTLY PLAYING:** {now_playing}')


@bot.command()
async def flynn(ctx):
    await ctx.send(cat_gif)


@bot.command()
async def flip(ctx):
    outcome = randint(0, 100)
    if outcome in [74]:
        await ctx.send(RANDOM_GIF)
    elif outcome in [69]:
        await ctx.send(f"Head")
    else:
        # await ctx.send(f"Heads {str(outcome)}") if outcome % 2 == 1 else await ctx.send(f"Tails {str(outcome)}")
        await ctx.send(f"Heads") if outcome % 2 == 1 else await ctx.send(f"Tails")


@bot.command()
async def meow(ctx):
    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="audio/meow.mp3"))
    except:
        ctx.voice_client.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="audio/meow.mp3"))



@bot.command()
async def boom(ctx):
    channel = ctx.author.voice.channel
    try:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="audio/boom.mp3"))
    except:
        ctx.voice_client.play(discord.FFmpegPCMAudio(
            executable="E:/FFmpeg/bin/ffmpeg.exe", source="audio/boom.mp3"))


@bot.command()
async def bruh(ctx):
    filename = 'images/bruh.png'
    with open(filename, "rb") as fh:
        to_send = discord.File(fh, filename=filename)
        await ctx.send(file=to_send)



@bot.command()
async def honest(ctx):
    filename = 'images/honest.png'
    with open(filename, "rb") as fh:
        to_send = discord.File(fh, filename=filename)
        await ctx.send(file=to_send)


@bot.command()
async def beatbox(ctx):
    filename = 'images/beatbox.jpg'
    with open(filename, "rb") as fh:
        to_send = discord.File(fh, filename=filename)
        await ctx.send(file=to_send)



@bot.command()
async def crump(ctx):
    filename = 'https://tenor.com/view/marge-simpson-dancing-homer-simpson-gif-12235449'
    await ctx.send(f'{filename}')


@bot.command()
async def monkey(ctx):
    await ctx.send('https://tenor.com/view/happy-monkey-circle-happy-monkey-circle-happy-monkey-circle-meme-gif-19448999')



@bot.command(name='commands', aliases=['c'])
async def commands(ctx, *args):
    if len(args) > 0:
        if args[0] in ['general', 'gen', 'g']:
            commands = ['!monkey', '!bruh', 
                         '!boom',  '!flip', '!flynn', '!beatbox',
                        '!honest', '!crump']
            to_send = '**List of Commands**:'
            num = 0
            for c in commands:
                to_send += '\n'
                num += 1
                to_send += f'{num}. {c}'
            await ctx.send(to_send)

        elif args[0] in ['bot', 'b']:
            commands = ['!play / !p', '!skip / !s',
                        '!nowplaying / !np', '!pause', '!resume']

            to_send = '**List of Commands**:'
            num = 0
            for c in commands:
                to_send += '\n'
                num += 1
                to_send += f'{num}. {c}'
            await ctx.send(to_send)

        elif args[0] in ['admin', 'ad']:
            commands = ['!clear', '!clear_all', '!register']
            to_send = '**List of Commands**:'
            num = 0
            for c in commands:
                to_send += '\n'
                num += 1
                to_send += f'{num}. {c}'
            await ctx.send(to_send)
    else:
        await ctx.send(f'Proper use is *!commands [topic]*')
        await ctx.send(f'Topics include: general, bot, admin')


@bot.command()
async def register(ctx):
    user_id = ctx.message.author.id
    with open('data.json', 'r') as fp:
        try:
            data = json.load(fp)
            for dic in data:
                if dic['id'] == str(user_id):
                    await ctx.send('This user is already registered.')
                    return
            dig_data = {'id': str(user_id), 'items': []}
            data.append(dig_data)
            fp.close()
            decider = 0
        except:
            dig_data = [{'id': str(user_id), 'items': []}]
            fp.close()
            decider = 1
    with open('data.json', 'w') as fp:
        if decider == 1:
            json.dump(dig_data, fp)
        else:
            json.dump(data, fp)
        fp.close()
    await ctx.send('This user has been registered.')


@bot.command()
async def ninja(ctx):
    # Dummy command to remove user from server.
    global confirm2
    print(ctx.message.author.id)
    if str(ctx.message.author.id) != '288461670479822849':
        confirm2 += 1
        user = ctx.author
        print(user)
        if confirm2 == 1:
            await ctx.send("Are you sure you want to say ninja?")
        elif confirm2 == 2:
            await ctx.send(f"You're not allowed to say that!! {str(user)}")
            await user.send('meow')
            await user.kick(reason='lol')
            confirm2 = 0
        
    else:
        await ctx.send(f"Get another user to type !ninja to gain 'Founder' Role.")


@bot.command()
async def dig(ctx):
    user = str(ctx.message.author.id)
    with open('data.json', 'r') as fp:
        # Verifying user is registered
        try:
            data = json.load(fp)
            print(data)
            pos = -1
            for dic in data:
                decider = 1 if dic['id'] == user else 0
                pos += 1
            fp.close()
            if decider == 1:
                print('Registered.')
            else:
                await ctx.send(f'{ctx.message.author} is not currently registered.')
                return
        except Exception as error:
            print(f'Error Occured: {error}')

    with open('data.json', 'w') as fp:
        # TODO: Run logic to find dug item

        item = dig_logic()
        try:
            await item
            data[pos]['items'].append(item)
            pass

        except Exception as error:
            print(f'Error Occured: {error}')
        json.dump(data, fp)
        fp.close()


# ESSENTIALS -------------------------------------------------------------------

@bot.command()
async def disconnect(ctx):
    for vc in bot.voice_clients:
        if vc.guild == ctx.message.guild:
            return await vc.disconnect()
    clear()
    return await ctx.send("Bot is not in any voice chat currently.")


@bot.command()
async def clear(ctx):
    global data
    global tasker
    global song_queue
    global now_playing
    data = {"guilds": []}
    tasker = None
    song_queue = []
    now_playing = ""
    return


@bot.command()
async def clear_all(ctx):
    if str(ctx.message.author) != 'Daruni#8443':
        await ctx.send('Only the server owner can clear all data.')
        return

    global confirm
    confirm += 1
    if confirm == 1:
        await ctx.send("Are you sure you want to delete all data? Run command again if so.")
    elif confirm == 2:
        os.remove('data.json')
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as fp:
                fp.close()
            await ctx.send("Data has been deleted.")
        confirm = 0

'''
@bot.event()
async def timeout(ctx):
    voice = ctx.message.guild.voice_client
    if voice != None:
        for vc in bot.voice_clients:
            if vc.guild == ctx.message.guild:
                if vc.channel.members < 1:
                    return await vc.disconnect()

    return
'''
# Helper Functions--------------------------------------------------------------


async def command_print(ctx, commands):
    to_send = '**List of Commands**:'
    num = 0
    for c in commands:
        to_send += '\n'
        num += 1
        to_send += f'{num}. {c}'
    return to_send


async def dig_logic():
    roll = randint(1, 1000)
    async with get_items() as all_items:
        print(all_items)
        return all_items
    # return asyncio.as_completed(get_items())
    # all_items = get_items()
    # await all_items
    # print(all_items)
    # return "Reuben's Plushie"

if __name__ == '__main__':
    bot.run(TOKEN)


# dig_data = [
#     {name: 'name', items: []}
# ]


'''
@bot.event
async def timeout():
    print("Checking timeout")
    for vc in bot.voice_clients:
        if vc.channel.members < 1:
            return await vc.disconnect()
    
'''
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




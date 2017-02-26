import discord
import asyncio
import random
import json
import time
import requests
import git
import subprocess
import sys
import os
import logging
import aiohttp
import base64
from datetime import datetime
import modules.commands as commands
import modules.misc as misc
import modules.pokemon as pokemon
import modules.admin as admin
import modules.embed_commands as embed_commands
import modules.google_search as google_search
import modules.owner as owner
import modules.random as random_cmds
import modules.voice as voice

from google import search

if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus('opus')
    except OSError:
        try:
            discord.opus.load_opus('libopus')
        except OSError:
            print('ERORR, Voice Will be disabled do to opus loading error')

if discord.opus.is_loaded():
    print('Voice Loaded!')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s: %(message)s')
try:
    with open("settings.json", "r") as infile:
        settings = json.loads(infile.read())
except:
    print('No Settings.json file located! please run setup.py first!')
    sys.exit()

with open("database/leave_toggle.json","r") as infile:
    leavemsg = json.loads(infile.read())

with open("database/quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/storage.json", "r") as infile:
    storage = json.loads(infile.read())

with open("database/storage2.json", "r") as infile:
    storage2 = json.loads(infile.read())
    
    
class Weenie(discord.Client):
    def __init__(self, *args, **kwargs):
        self.timer = 0
        self.suspend = False
        self.repl = False
        self.voiceMap = {}
        self.voiceQ = {}
        super().__init__(*args, **kwargs) 

status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'
client = Weenie()
gamet = discord.Game(name='With Computers')
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)

@client.event
async def on_ready():
    client.bot_info = await client.application_info()
    print('Bot owner:\n' + client.bot_info.owner.id)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('<Servers>')
    for server in client.servers:
        print(server)
    print('------')
    await client.change_presence(game=gamet, status='online', afk=False)
    if client.bot_info.owner.id not in admin:
        admin.append(client.bot_info.owner.id)

@client.event
async def on_member_ban(member):
    if leavemsg[member.server.id] == 1:
        for i in channel.server.channels:
            if i.name == 'logs':
                    await client.send_message(i, '{} Has just been banned from the server :( Bye!'.format(member.name))
        try:
            await client.send_message(member.server.default_channel, '{} Has just been banned from the server :( Bye!'.format(member.name))
        except:
            pass

@client.event
async def on_server_join(server):
    await client.send_message(server, 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type `!help` to see what I can do for you!')

@client.event
async def on_channel_delete(channel):
    for i in channel.server.channels:
        if i.name == 'logs':
            r = lambda: random.randint(0,255)
            rr = ('0x%02X%02X%02X' % (r(),r(),r()))
            cd_details = discord.Embed(title='Channel Deleted!', description='', colour=int(rr, 16))
            cd_details.add_field(name='Channel Name:', value=channel.name, inline=True)
            cd_details.add_field(name='Channel ID:', value=channel.id, inline=True)
            cd_details.add_field(name='Channel Topic:', value=channel.topic, inline=True)
            cd_details.set_author(name='Removed channel...', icon_url=message.author.avatar_url)
            await client.send_message(i, embed=cd_details)   


@client.event
async def on_channel_create(channel):
    for i in channel.server.channels:
        if i.name == 'logs':
            r = lambda: random.randint(0,255)
            rr = ('0x%02X%02X%02X' % (r(),r(),r()))
            cc_details = discord.Embed(title='Channel Created!', description='', colour=int(rr, 16))
            cc_details.add_field(name='Channel Name:', value=channel.name, inline=True)
            cc_details.add_field(name='Channel ID:', value=channel.id, inline=True)
            cc_details.add_field(name='Channel Topic:', value=channel.topic, inline=True)
            cc_details.set_author(name='New channel...', icon_url=message.author.avatar_url)
            await client.send_message(i, embed=cc_details)   

@client.event
async def on_message_edit(before, after):
    for i in before.server.channels:
        if i.name == 'logs':
            r = lambda: random.randint(0,255)
            rr = ('0x%02X%02X%02X' % (r(),r(),r()))
            em_details = discord.Embed(title='Message Edited!', description='', colour=int(rr, 16))
            em_details.add_field(name='Author:', value=before.author, inline=True)
            em_details.add_field(name='Before:', value=before.content, inline=True)
            em_details.add_field(name='After:', value=after.content, inline=True)
            em_details.set_author(name='Edited message...', icon_url=before.author.avatar_url)
            await client.send_message(i, embed=em_details)   

@client.event
async def on_message_delete(message):
    for i in message.server.channels:
        if i.name == 'logs':
            r = lambda: random.randint(0,255)
            rr = ('0x%02X%02X%02X' % (r(),r(),r()))
            md_details = discord.Embed(title='Message Deleted!', description='', colour=int(rr, 16))
            md_details.add_field(name='Author:', value=message.author, inline=True)
            md_details.add_field(name='Message:', value=message.content, inline=True)
            md_details.set_author(name='Deleted message...', icon_url=message.author.avatar_url)
            await client.send_message(i, embed=md_details)   

@client.event
async def on_member_join(member):
    with open("database/storage2.json", "r") as infile:
        storage2 = json.loads(infile.read())
    if member.server.id not in storage2:
        storage2[member.server.id] = 'message0'
    with open("database/storage2.json", "w+") as outfile:
        outfile.write(json.dumps(storage2))
    
    if storage2[member.server.id] == 'message0':
        try:
            for i in member.server.channels:
                if i.name == 'logs':
                    await client.send_message(i, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    
            try:
                await client.send_message(member.server.default_channel,"{0.name} has joined {0.server.name} give them a warm welcome!".format(member))    
            except discord.Forbidden:
                print('Couldn\'t welcome {} in server {} due to perms error.'.format(member, member.server))
        except discord.Forbidden:
            print('Couldn\'t welcome {} in server {} due to perms error.'.format(member, member.server))

@client.event  
async def on_member_remove(member):
    if leavemsg[member.server.id] == 1:
        for i in member.server.channels:
            if i.name == 'logs':
                r = lambda: random.randint(0,255)
                rr = ('0x%02X%02X%02X' % (r(),r(),r()))
                rm_details = discord.Embed(title='Member left!', colour=int(rr, 16))
                rm_details.add_field(name='Username:', value=member.name, inline=True)
                rm_details.add_field(name='Nick:', value=member.nick, inline =True)
                rm_details.add_field(name='Joined Server:', value=member.joined_at.strftime(x33), inline =True)
                rm_details.add_field(name='Account Created:', value=member.created_at.strftime(x33), inline=True)
                rm_details.set_author(name='We lost a member :(', icon_url=member.server.get_member_named(username).avatar_url)
                await client.send_message(i, embed=rm_details)    
        try:
            await client.send_message(member.server.default_channel, "{0.name} has left {0.server.name} we will miss you!".format(member))    
        except:
            pass
@client.event
async def on_message(message):
    try:
        if message.server.id not in client.voiceQ:
            client.voiceQ[message.server.id] = Voice = voice.Voice(client)
    except:
        print('Errored: Most likely due to Private DM\'s')

    try:
        for channel in message.server.channels:
            if str(channel.type) == 'voice':
                client.voiceMap[channel.name] = channel.id
    except:
        pass    
    with open("database/prefixMap.json", "r") as infile:
        prefixMap = json.loads(infile.read())
    
    try:
        if message.server.id not in storage:
            storage[message.server.id] = 'broadcast0'
    except:
        pass        
    with open("database/storage.json", "w+") as outfile:
        outfile.write(json.dumps(storage))
    try:
        if message.server.id not in leavemsg:
            leavemsg[message.server.id] = '1'
    except:
        pass        
    with open("database/storage.json", "w+") as outfile:
        outfile.write(json.dumps(storage))

    try:
        if message.server.id not in prefixMap:
            prefixMap[message.server.id] = '!'
            client.pfix = prefixMap[message.server.id]
        else:
            client.pfix = prefixMap[message.server.id]
    except:
        print('Errored: Most likely due to Private DM\'s')
    
    if message.content.startswith(client.pfix)  and client.suspend == False and message.author.bot is False:
        try:
            if message.content == client.pfix + 'quote' :
                await misc.rand_quote(message, client)
            elif message.content.split(' ')[0] == client.pfix + 'quote':
                await misc.quote_logic(message, client)
            else:
                cmd = bdel(message.content.lower(), client.pfix)
                cmd = cmd.split(' ')
                for i in commands.cmdDict.keys():
                    if cmd[0] in i:
                        await commands.cmdDict[i](message, client)
        except KeyError as e:
            print(str(e) + ' No command')
                
    if message.content == client.pfix + 'resume' and client.suspend == True:
        await commands.resume_logic(message, client)
        
    if message.content.startswith(client.pfix + 'skip'):
        await client.voiceQ[message.server.id].skip(message, client)
        
    if message.content.startswith(client.pfix + 'join'):
        await client.voiceQ[message.server.id].join(message, client)

    if message.content.startswith(client.pfix + 'play'):
        await client.voiceQ[message.server.id].play(message, client)

    if message.content.startswith(client.pfix + 'stop'):
        await client.voiceQ[message.server.id].stop(message, client)

    if message.content.startswith(client.pfix + 'pause'):
        await client.voiceQ[message.server.id].pause(message, client)

    if message.content.startswith(client.pfix + 'unpause'):
        await client.voiceQ[message.server.id].mresume(message, client)

    if message.content.startswith(client.pfix + 'disconnect'):
        await client.voiceQ[message.server.id].disconnect(message, client)

    if message.content.startswith(client.pfix + 'volume'):
        await client.voiceQ[message.server.id].volume(message, client)

    if message.content.startswith(client.pfix + 'nowplaying'):
        await client.voiceQ[message.server.id].playing(message, client)

    if message.content.lower().startswith('weeniebot'):
                await commands.cleverbot_logic(message, client)
    if message.content == "!prefix":
        await misc.get_prefix_logic(message, client)

    if message.content == client.pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')

client.run(settings['token'])

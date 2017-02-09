import discord
import asyncio
import random
import json
import time
import cleverbot
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
import modules.botToken as botToken
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

logging.basicConfig(level=logging.INFO)

with open("database/prefix.json", "r") as infile:
    prefix = json.loads(infile.read())

with open("database/quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/storage.json", "r") as infile:
    storage = json.loads(infile.read())

with open("database/storage2.json", "r") as infile:
    storage2 = json.loads(infile.read())
    
with open("database/quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))

with open("database/adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))
    
with open("database/prefix.json", "w+") as outfile:
    outfile.write(json.dumps(prefix))

with open("database/storage2.json", "w+") as outfile:
    outfile.write(json.dumps(storage2))
with open("database/storage.json", "w+") as outfile:
    outfile.write(json.dumps(storage))
    
class Weenie(discord.Client):
    def __init__(self, *args, **kwargs):
        self.timer = 0
        self.suspend = False
        self.repl = False
        self.voiceMap = {}
        super().__init__(*args, **kwargs) 

status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'
client = Weenie()
cb1 = commands.cb1
gamet = discord.Game(name='beefywhale.github.io/WeenieBot/')
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)

@client.event
async def on_ready():
    client.bot_info = await client.application_info()
    print(str(client.bot_info.owner.id))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('<Servers>')
    for server in client.servers:
        print(server)
    print('------')
    await client.change_presence(game=gamet, status='online', afk=False)
    try:
        await client.change_nickname(message.server.me, 'WeenieBot')
    except:
        pass
    
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
            await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    
        except discord.Forbidden:
            print('Couldn\'t welcome {} in server {} do to perms error.'.format(member, member.server))
        
@client.event
async def on_message(message):
    try:
        for channel in message.server.channels:
            if str(channel.type) == 'voice':
                client.voiceMap[channel.name] = channel.id
    except:
        print('Errored: Most likely due to Private DM\'s')
    
    with open("database/prefixMap.json", "r") as infile:
        prefixMap = json.loads(infile.read())
    
    try:
        if message.server.id not in storage:
            storage[message.server.id] = 'broadcast0'
    except:
        print('Errored: Most likely due to Private DM\'s')
        
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
    
    if message.content.startswith(client.pfix)  and client.suspend == False and str(message.author) != str(client.user):
        try:
            if message.content == client.pfix + 'quote' :
                await commands.rand_quote(message, client)
            elif message.content.split(' ')[0] == client.pfix + 'quote':
                await commands.quote_logic(message, client)
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
        
    if message.content.startswith(client.pfix + 'join'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.join(message, client)
    if message.content.startswith(client.pfix + 'play'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')        
        #await Voice.play(message, client)
    if message.content.startswith(client.pfix + 'stop'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.stop(message, client)
    if message.content.startswith(client.pfix + 'pause'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.pause(message, client)
    if message.content.startswith(client.pfix + 'unpause'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.mresume(message, client)
    if message.content.startswith(client.pfix + 'disconnect'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.disconnect(message, client)
    if message.content.startswith(client.pfix + 'volume'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.volume(message, client)
    if message.content.startswith(client.pfix + 'nowplaying'):
        await client.send_message(message.channel, 'All Music commands are disabled due to a flaw!')
        #await Voice.playing(message, client)
    
    if message.content == "!prefix":
        await commands.get_prefix(message, client)

    if message.content == client.pfix + 'jfgi':
        await client.send_message(message.channel, 'http://www.justfuckinggoogleit.com/')

    if message.content == client.pfix + 'good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')

    if message.content == client.pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type ' + client.pfix + 'help to see what I can do for you!')

client.run(botToken.token)

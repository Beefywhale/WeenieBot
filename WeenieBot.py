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
import uvloop
import aiohttp
from datetime import datetime
import modules.commands as commands
import modules.botToken as botToken
from google import search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=logging.INFO)

with open("prefix.json", "r") as infile:
    prefix = json.loads(infile.read())

with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))

with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))
    
with open("prefix.json", "w+") as outfile:
    outfile.write(json.dumps(prefix))

class Weenie(discord.Client):
    def __init__(self, *args, **kwargs):
        self.timer = 0
        self.suspend = False
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
    if member.server.id != '110373943822540800':
        await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    

@client.event
async def on_error(error, *e_args, **e_kwargs):
    print('Discord errored! the error was: ' + error)
        
@client.event
async def on_message(message):
    with open("database/prefixMap.json", "r") as infile:
        prefixMap = json.loads(infile.read())
    if message.server.id not in prefixMap:
        prefixMap[message.server.id] = '!'
        client.pfix = prefixMap[message.server.id]
    else:
        client.pfix = prefixMap[message.server.id]
    
    if message.content.startswith(client.pfix)  and client.suspend == False:
        try:
            if message.content == client.pfix + 'quote' :
                await commands.rand_quote(message, client)
            elif message.content.split(' ')[0] == client.pfix + 'quote':
                await commands.quote_logic(message, client)
            else:
                cmd = bdel(message.content.lower(), client.pfix)
                cmd = cmd.split(' ')
                await commands.cmdDict[cmd[0]](message, client)
        except KeyError as e:
            print(str(e) + ' No command')

    if message.content.lower().startswith('weeniebot'):
        await commands.cleverbot_logic(message, client)
    elif message.content.lower().startswith('wb'):
        await commands.cleverbot_logictwo(message, client)
                
    if message.content == client.pfix + 'resume' and client.suspend == True:
        await commands.resume_logic(message, client)
    
    if message.content == "prefix":
        await commands.get_prefix(message, client)

    if message.content == client.pfix + 'jfgi':
        await client.send_message(message.channel, 'http://www.justfuckinggoogleit.com/')

    if message.content == client.pfix + 'good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')

    if message.content == client.pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type ' + pfix + 'help to see what I can do for you!')

client.run(botToken.token)


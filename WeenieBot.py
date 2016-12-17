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
pfix = commands.pfix
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('<Members>')
    for server in client.servers:
        for member in server.members:
            print(member)
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
    if member.server.id == '110373943822540800':
        await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    

@client.event
async def on_message(message):
    with open("prefix.json", "r") as infile:
        prefix = json.loads(infile.read())
    pfix = commands.pfix

    if message.content.startswith(pfix):
        try:
            if message.content == pfix + 'quote':
                await commands.rand_quote(message, client)
            elif message.content.split(' ')[0] == pfix + 'quote':
                await commands.quote_logic(message, client)
            else:
                cmd = bdel(message.content.lower(), pfix)
                cmd = cmd.split(' ')
                await commands.cmdDict[cmd[0]](message, client)
        except Exception as e:
            print(str(e) + ' No command')

    if message.content.lower().startswith('~!weeniebot'):
        if message.author.bot:
            pass
        else:
            await commands.cleverbot_logic(message, client)

    if message.content == pfix + 'ping':
        await client.send_message(message.channel, 'Pong')

    if message.content == pfix + 'update':
        if message.author.name in prefix["bot_owner"]:
            await client.send_message(message.channel, 'Updating...')
            g = git.cmd.Git()
            u = g.pull('-v')
            await client.send_message(message.channel, '```' + str(u) + '```')
            if str(u) == 'Already up-to-date.':
                await client.send_message(message.channel, 'Already Up To Date! Not restarting')
            else:
                await client.send_message(message.channel, 'Update successful restarting!')
                os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await client.send_message(message.channel, 'Error Didn\'t update maybe you aren\'t an admin?')

    if message.content == pfix + 'jfgi':
        await client.send_message(message.channel, 'http://www.justfuckinggoogleit.com/')

    if message.content == pfix + 'good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')

    if message.content == pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')

    if message.content.lower() == '~!hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type ' + pfix + 'help to see what I can do for you!')

    if message.content == pfix + 'help':
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='', colour=int(rr, 16))
        help_details.add_field(name='__**Quotes**:__', value='\n'+
'\n' + pfix + 'quote --- picks a random quote to tell everyone.\n'+
'\n' + pfix + 'quote <number> --- picks a specific quote to tell everyone.\n'+
'\n' + pfix + 'quoteadd --- adds a new quote\n'+
'\n' + pfix + 'delquote <number> --- deletes specific quote\n'+
'\n' + pfix + 'editquote <number> --- next message you send changes the quote you specified\n', inline=True)


        help_details.add_field(name='__**Random**:__', value='\n'+
'\n' + pfix + 'sleep --- bot goes to sleep for 5 seconds.\n'+
'\n' + pfix + 'jfgi --- just fucking google it.\n'+
'\n' + pfix + 'googlefight <entry 1> <entry 2> --- generates a google fight link too see what is searched more.(use + for spaces EX: !googlefight Space+Jam Smash+Mouth)\n'+
'\n' + pfix + 'messages --- tells you how many messages there are in the channel you are in.\n', inline=True)

        help_details.add_field(name='__**Admin**:__', value='\n'+
'\n' + pfix + 'admintest --- check if you are admin!\n'+
'\n' + pfix + 'deladmin --- deletes admin by user name.\n'+
'\n' + pfix + 'addadmin <Persons Discord Name> --- adds admin by user name.\n', inline=True)

        help_details.add_field(name='__**Bot Owner**:__', value='\n'+
'\n' + pfix + 'update --- updates bot to newest version! (do this frequently!!!)\n', inline=True)

        help_details.add_field(name='__**WeenieBot**:__', value='\n'+
'\n' + pfix + 'hello weeniebot --- bot greets you.\n'+
'\n' + pfix + 'WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)\n', inline=True)

        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, embed=help_details)



client.run(botToken.token)


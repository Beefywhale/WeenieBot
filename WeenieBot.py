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
import modules.commands as commands
import modules.botToken as botToken
from google import search

#changes! testing updates heehee

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


status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'

client = discord.Client()
#cb1 = commands.cb1
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
    print('------')
    await client.change_presence(game=gamet, status='online', afk=False)



@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    

@client.event
async def on_message(message):
    with open("prefix.json", "r") as infile:
        prefix = json.loads(infile.read())
    pfix = commands.pfix
    await client.change_nickname(message.server.me, 'WeenieBot')

    if message.content.startswith(pfix + "setprefix"):
        await commands.prefix_logic(message, client)

    
    if message.content == pfix + 'hotdog':
        await commands.hotdog(message, client)
    
    if message.content.lower().startswith('weeniebot'):
        await commands.cleverbot_logic(message, client)
        
    if message.content == 'prefix':
        await commands.get_prefix(message, client)
        
    if message.content.lower().startswith('wb'):
        await commands.cleverbot_logic2(message, client)
        
    if message.content == pfix + 'messages':
        await commands.user_messages(message, client)
        
    if message.content == pfix + 'purge':
        await purge(message, client)

    if message.content == pfix + 'ping':
        await client.send_message(message.channel, 'Pong')
        
    if message.content == pfix + 'update':
        if message.author.name in admin:
            g = git.cmd.Git()
            u = g.pull('-v')
            await client.send_message(message.channel, '```' + str(u) + '```')
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await client.send_message(message.channel, 'Error Didn\'t update maybe you aren\'t an admin?')
       
    if message.content.startswith(pfix + 'user'):
        await commands.user(message, client)

    if message.content == pfix + 'admins':
        await commands.admin_amount(message, client)

    if message.content.startswith(pfix + 'pokedex'):
        await commands.getPokemon(message, client)

    if message.content == pfix + 'pokemon':
        await commands.randPokemon(message, client)

    if message.content.startswith(pfix + 'google'):
        await commands.google_search(message, client)

    if message.content.startswith(pfix + 'googlefight'):
        await commands.google_Fight(message, client)

    if message.content == pfix + 'jfgi':
        await client.send_message(message.channel, 'http://www.justfuckinggoogleit.com/')
        
    if message.content == pfix + 'good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')
    
    if message.content.startswith(pfix + 'sleep'):
        await commands.sleep(message, client)

    if message.content == pfix + 'quotes':
        await commands.quote_amount(message, client)

    if commands.timer == 0 and message.content == pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')
        commands.timer = 1
    elif  commands.timer == 1 and message.content == pfix + 'turtles':
        commands.cooldown(message, client)

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type !help to see what I can do for you!')

    if message.content == pfix + 'quoteadd':
        await commands.quoteadd_logic(message, client)


    if commands.timer == 0 and message.content == pfix + 'quote':
        await commands.rand_quote(message, client)
    elif  commands.timer == 1 and message.content == pfix + 'quote':
        await commands.cooldown(message, client)

    if message.content.startswith(pfix + 'delquote'):
        await commands.delquote_logic(message, client)

    if message.content.startswith(pfix + 'editquote'):    
        await commands.editquote_logic(message, client)

    if commands.timer == 0 and message.content.split(' ')[0] == pfix + 'quote':
        await commands.quote_logic(message, client)
    elif commands.timer == 1 and message.content.split(' ')[0] == pfix + 'quote':
        open("quoteweenie.json", "r")
        try:
            try:
                commands.cooldown(message, client)
            except ValueError:
                pass
        except IndexError:
            await client.send_message(message.channel, 'That quote doesn\'t exist!')

    if message.content == pfix + 'addadmin':
        await commands.add_admin_logic(message, client)

    if message.content.startswith(pfix + 'deladmin'):
        await commands.deladmin_logic(message, client)

    if message.content.startswith(pfix + 'admintest'):
        await commands.admintest(message, client)

    if message.content == pfix + 'help':
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='''
!quote --- picks a random quote to tell everyone.
!quote <number> --- picks a specific quote to tell everyone.
!quoteadd --- adds a new quote
!delquote <number> --- deletes specific quote
!editquote <number> --- next message you send changes the quote you specified


!sleep --- bot goes to sleep for 5 seconds.
!jfgi --- just fucking google it.
!googlefight <entry 1> <entry 2> --- generates a google fight link too see what is searched more.(use + for spaces EX: !googlefight Space+Jam Smash+Mouth)
!messages --- tells you how many messages there are in the channel you are in.

!admintest --- check if you are admin!
!deladmin --- deletes admin by user name.
!addadmin <Persons Discord Name> --- adds admin by user name.

!update --- updates bot to newest version! (do this frequently!!!)

hello weeniebot --- bot greets you.
WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)''', colour=int(rr, 16))
        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, embed=help_details)



client.run(botToken.token)

def main():
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


    status = {
        'online': 'Online',
        'offline': 'Offline',
        'idle': 'Idle',
        'dnd': 'Do Not Disturb'
    }

    x33 = '%m-%d-%Y'

    client = discord.Client()
    gamet = discord.Game(name='beefywhale.github.io/WeenieBot/')
    pfix = commands.pfix
    client.run(botToken.token)
    
if __name__ == '__main__': main()

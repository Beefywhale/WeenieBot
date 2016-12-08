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

with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))

with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))

with open("prefix.json", "r") as infile:
    prefix = json.loads(infile.read())
with open("prefix.json", "w+") as outfile:
    outfile.write(json.dumps(prefix))


status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'

counter1 = len(Quotes_All)
counter2 = len(Quotes_All) - 1
timer = 0
client = discord.Client()
cb1 = cleverbot.Cleverbot()
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)

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


@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    

@client.event
async def on_message(message):
    global timer
    open("prefix.json", "r")
    pfix = prefix["prefix"]
    await client.change_nickname(message.server.me, 'WeenieBot')

    if message.content.lower().startswith('weeniebot'):
        await commands.cleverbot_logic(message, client)

    if message.content.startswith(pfix + 'setprefix'):
        open("prefix.json", "r")
        await commands.prefixfunc(message, client)
        
    if message.content == pfix + 'messages':
        await commands.user_messages(message, client)
        
    if message.content == pfix + 'purge':
        await purge(message, client)

    if message.content == pfix + 'update':
        g = git.cmd.Git()
        u = g.pull('-v')
        await client.send_message(message.channel, str(u))
        os.execl(sys.executable, sys.executable, *sys.argv)
       
    if message.content.startswith(pfix + 'user'):
        await commands.user(message, client)

    if message.content == pfix + 'admins':
        await commands.admin_amount(message, client)

    if message.content.startswith(pfix + 'pokemon'):
        await commands.getPokemonData(message, client)

    if message.content.startswith(pfix + 'google'):
        await commands.google_search(message, client)

    if message.content == pfix + 'good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')
    
    if message.content.startswith(pfix + 'sleep'):
        await commands.sleep(message, client)

    if message.content == pfix + 'quotenumber':
        await commands.quote_amount(message, client)

    if timer == 0 and message.content == pfix + 'turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')
        timer = 1
    elif  timer == 1 and message.content == pfix + 'turtles':
        commands.cooldown(message, client)

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type !help to see what I can do for you!')


    if message.content == pfix + 'quoteadd':
        await commands.quoteadd_logic(message, client)


    if timer == 0 and message.content == pfix + 'quote':
        await commands.rand_quote(message, client)
    elif  timer == 1 and message.content == pfix + 'quote':
        await commands.cooldown(message, client)

    if message.content.startswith(pfix + 'delquote'):
        try:
            del_quote = int(message.content.strip(pfix + 'delquote '))
            if message.author.name in admin:
                try:
                    await client.send_message(message.channel, 'Quote {} Deleted'.format(del_quote))
                    del Quotes_All[del_quote]
                    with open("quoteweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(Quotes_All))
                except IndexError:
                    await client.send_message(message.channel, 'That quote doesn\'t exist!')
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')
        except:
            pass

        if message.content.startswith(pfix + 'editquote'):
            edit_quote = int(message.content.strip(pfix + 'editquote '))
            if message.author.name in admin:
                try:
                    await client.send_message(message.channel, 'Editing Quote {}'.format(edit_quote))
                    msg = await client.wait_for_message(author=message.author)
                    Quotes_All[edit_quote] = msg.content
                    await client.send_message(message.channel, 'Quote Edited')
                    with open("quoteweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(Quotes_All))
                except IndexError:
                    await client.send_message(message.channel, 'That quote doesn\'t exist!')
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')

    if timer == 0 and message.content.split(' ')[0] == pfix + 'quote':
        try:
            try:
                open("quoteweenie.json","r")
                quote_number = int(message.content.strip(pfix + 'quote '))
                print(quote_number)
                await client.send_message(message.channel, Quotes_All[quote_number])
                timer = 1
                await asyncio.sleep(8)
                timer = 0
            except IndexError:
                await client.send_message(message.channel, 'That quote doesn\'t exist!')
        except ValueError:
            pass
    elif timer == 1 and message.content.split(' ')[0] == pfix + 'quote':
        try:
            try:
                quote_number = int(message.content.strip(pfix + 'quote '))
                print('COOLDOWN')
                await client.send_message(message.author, '10 second Command Cooldown please be patient and don\'t spam commands! :)')
                await asyncio.sleep(2)
                timer = 0
            except ValueError:
                pass
        except IndexError:
            await client.send_message(message.channel, 'That quote doesn\'t exist!')

    if message.content == pfix + 'addadmin':
        await commands.add_admin_logic(message, client)

    if message.content.startswith(pfix + 'deladmin'):
        try:
            del_admin = str(message.content.replace(pfix + 'deladmin ', ''))
            if message.author.name in admin:
                if del_admin in admin:
                    await client.send_message(message.channel, 'Admin Removed')
                    admin.remove(del_admin)
                    with open("adminweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(admin))
                else:
                    await client.send_message(message.channel, 'ERROR {} was never an Admin!'.format('`' + del_admin + '`'))
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')
        except:
            pass

    if message.content.startswith(pfix + 'admintest'):
        open("adminweenie.json","r")
        if message.author.name in admin:
            await client.send_message(message.channel, 'Hello Admin!')
        elif message.author.name not in admin:
            await client.send_message(message.channel, 'Not Admin!')

    if message.content == pfix + 'help':
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='''
pfix + quote --- picks a random quote to tell everyone.
pfix + quote <number> --- picks a specific quote to tell everyone.
pfix + quoteadd --- adds a new quote
pfix + delquote <number> --- deletes specific quote
pfix + sleep --- bot goes to sleep for 5 seconds.
pfix + messages --- tells you how many messages there are in the channel you are in.
pfix + admintest --- check if you are admin!
pfix + deladmin --- deletes admin by user id
pfix + addadmin <Persons Discord ID>--- adds admin by user id
hello weeniebot --- bot greets you.
WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)''', colour=int(rr, 16))
        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, embed=help_details)



client.run(botToken.token)


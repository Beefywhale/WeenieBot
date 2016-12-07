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
    await client.change_nickname(message.server.me, 'WeenieBot')

    if message.content.lower().startswith('weeniebot'):
        await commands.cleverbot_logic(message)

    if message.content == '!messages':
        await commands.user_messages(message)

    if message.content == '!purge':
        await purge(message)

    if message.content == '!update':
        g = git.cmd.Git()
        u = g.pull('-v')
        await client.send_message(message.channel, str(u))
        os.execl(sys.executable, sys.executable, *sys.argv)
       
    if message.content.startswith('!user'):
        await commands.user(message)

    if message.content == '!admins':
        await commands.admin_amount(message)

    if message.content.startswith('!pokemon'):
        await commands.getPokemonData(message)

    if message.content.startswith('!google'):
        await commands.google_search(message)

    if message.content == '!good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')
    
    if message.content.startswith('!sleep'):
        await commands.sleep(message)

    if message.content == '!quotenumber':
        await commands.quote_amount(message)

    if timer == 0 and message.content == '!turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')
        timer = 1
    elif  timer == 1 and message.content == '!turtles':
        commands.cooldown(message)

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type !help to see what I can do for you!')


    if message.content == '!quoteadd':
        await commands.quoteadd_logic(message)


    if timer == 0 and message.content == '!quote':
        await commands.rand_quote(message)
    elif  timer == 1 and message.content == '!quote':
        await commands.cooldown(message)

    if message.content.startswith('!delquote'):
        try:
            del_quote = int(message.content.strip('!delquote '))
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

        if message.content.startswith('!editquote'):
            edit_quote = int(message.content.strip('!editquote '))
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

    if timer == 0 and message.content.split(' ')[0] == '!quote':
        try:
            try:
                open("quoteweenie.json","r")
                quote_number = int(message.content.strip('!quote '))
                print(quote_number)
                await client.send_message(message.channel, Quotes_All[quote_number])
                timer = 1
                await asyncio.sleep(8)
                timer = 0
            except IndexError:
                await client.send_message(message.channel, 'That quote doesn\'t exist!')
        except ValueError:
            pass
    elif timer == 1 and message.content.split(' ')[0] == '!quote':
        try:
            try:
                quote_number = int(message.content.strip('!quote '))
                print('COOLDOWN')
                await client.send_message(message.author, '10 second Command Cooldown please be patient and don\'t spam commands! :)')
                await asyncio.sleep(2)
                timer = 0
            except ValueError:
                pass
        except IndexError:
            await client.send_message(message.channel, 'That quote doesn\'t exist!')

    if message.content == '!addadmin':
        await commands.add_admin_logic(message)

    if message.content.startswith('!deladmin'):
        try:
            del_admin = str(message.content.replace('!deladmin ', ''))
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

    if message.content.startswith('!admintest'):
        open("adminweenie.json","r")
        if message.author.name in admin:
            await client.send_message(message.channel, 'Hello Admin!')
        elif message.author.name not in admin:
            await client.send_message(message.channel, 'Not Admin!')

    if message.content == '!help':
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='''
!quote --- picks a random quote to tell everyone.
!quote <number> --- picks a specific quote to tell everyone.
!quoteadd --- adds a new quote
!delquote <number> --- deletes specific quote
!sleep --- bot goes to sleep for 5 seconds.
!messages --- tells you how many messages there are in the channel you are in.
!admintest --- check if you are admin!
!deladmin --- deletes admin by user id
!addadmin <Persons Discord ID>--- adds admin by user id
hello weeniebot --- bot greets you.
WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)''', colour=int(rr, 16))
        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, embed=help_details)



client.run(botToken.token)